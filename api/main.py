"""
AI Decision Engine API - FastAPI Implementation
Main API server with enhanced error handling and validation
"""

from fastapi import FastAPI, Header, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
import os
import logging
import traceback

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import our existing decision engine
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_decision_engine import AIDecisionEngine, DecisionCategory, RiskLevel

app = FastAPI(
    title="AI Decision Engine API",
    description="RESTful API for AI-driven decision-making framework",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - configure for production
cors_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if "*" not in cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Analytics middleware
from api.analytics_middleware import AnalyticsMiddleware
app.add_middleware(AnalyticsMiddleware)

# Initialize decision engine
try:
    decision_engine = AIDecisionEngine()
    logger.info("Decision engine initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize decision engine: {e}")
    raise

# Import API key manager and analytics
from api.api_key_manager import api_key_manager
from api.analytics import api_analytics
import time

# API Key authentication
def verify_api_key(x_api_key: Optional[str] = Header(None, alias="X-API-Key")) -> Dict[str, Any]:
    """
    Verify API key from header
    
    Args:
        x_api_key: API key from X-API-Key header
    
    Returns:
        API key information if valid
    
    Raises:
        HTTPException: If API key is invalid or missing
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Include X-API-Key header."
        )
    
    # Validate API key
    key_info = api_key_manager.validate_api_key(x_api_key)
    
    if not key_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key"
        )
    
    # Record request for rate limiting
    api_key_manager.record_request(x_api_key)
    
    # Return key info
    return {
        "tier": key_info.get("tier", "free"),
        "requests_per_month": key_info.get("requests_per_month", 100),
        "api_key": x_api_key[:10] + "..."  # Partial key for logging
    }


# Pydantic models for request validation
class DecisionEvaluationRequest(BaseModel):
    category: str = Field(..., description="Decision category")
    amount: float = Field(default=0.0, ge=0, description="Amount involved")
    description: str = Field(default="", max_length=1000, description="Decision description")
    
    @validator('category')
    def validate_category(cls, v):
        valid_categories = [cat.name for cat in DecisionCategory]
        if v.upper() not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return v.upper()


class RiskAssessmentRequest(BaseModel):
    amount: float = Field(default=0.0, ge=0, description="Amount involved")
    category: str = Field(default="OPERATIONAL", description="Decision category")
    description: str = Field(default="", max_length=1000, description="Risk assessment description")
    
    @validator('category')
    def validate_category(cls, v):
        valid_categories = [cat.name for cat in DecisionCategory]
        if v.upper() not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return v.upper()


class AutoExecuteRequest(BaseModel):
    task_type: str = Field(..., description="Type of task")
    risk_level: str = Field(default="LOW", description="Risk level")
    
    @validator('risk_level')
    def validate_risk_level(cls, v):
        valid_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Risk level must be one of: {', '.join(valid_levels)}")
        return v.upper()


class MemoryInsightsRequest(BaseModel):
    decision_data: Dict[str, Any] = Field(default_factory=dict, description="Decision data for insights")


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
            "message": "Invalid request data"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Root endpoint - serves HTML landing page for browsers, JSON for API clients
    """
    # Check if request is from a browser (has Accept: text/html) or API client
    accept_header = request.headers.get("accept", "")
    
    if "text/html" in accept_header.lower():
        # Serve HTML landing page for browsers
        try:
            landing_path = os.path.join(os.path.dirname(__file__), "landing.html")
            with open(landing_path, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        except FileNotFoundError:
            # Fallback to JSON if HTML file not found
            pass
    
    # Return JSON for API clients
    return JSONResponse(content={
        "message": "AI Decision Engine API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs",
        "health": "/health",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
            "evaluate_decision": "/decisions/evaluate",
            "assess_risk": "/risk/assess",
            "autonomy_level": "/autonomy/level",
            "pricing": "/pricing"
        }
    })


@app.get("/health")
async def health_check():
    """Health check endpoint with detailed system status"""
    try:
        # Check decision engine status
        autonomy_status = decision_engine.autonomy.get_autonomy_level()
        
        return {
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "autonomy_level": autonomy_status,
            "system": "operational"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@app.post("/decisions/evaluate", response_model=Dict[str, Any])
async def evaluate_decision(
    decision_request: DecisionEvaluationRequest,
    api_info: Dict[str, Any] = Depends(verify_api_key)
):
    """
    Evaluate a decision using AI decision-making framework
    
    - **category**: Decision category (STRATEGIC, OPERATIONAL, FINANCIAL, etc.)
    - **amount**: Amount involved (default: 0)
    - **description**: Description of the decision
    """
    try:
        logger.info(f"Evaluating decision: {decision_request.category} - ${decision_request.amount}")
        
        # Convert to decision data format
        decision_data = {
            "category": decision_request.category,
            "amount": decision_request.amount,
            "description": decision_request.description
        }
        
        # Convert category string to enum value
        category_str = decision_data.get("category", "OPERATIONAL")
        decision_data["category"] = DecisionCategory[category_str].value if category_str in DecisionCategory.__members__ else category_str
        
        # Evaluate decision
        result = decision_engine.evaluate_decision(decision_data)
        
        # Convert to JSON-serializable format
        response = {
            "id": result.get("id"),
            "timestamp": result.get("timestamp"),
            "category": result.get("category"),
            "risk_level": result.get("risk_level"),
            "description": result.get("description"),
            "amount": result.get("amount"),
            "status": result.get("status"),
            "action_required": result.get("action_required"),
            "ai_can_decide": result.get("ai_can_decide"),
            "autonomy_level": result.get("autonomy_level"),
            "memory_insights": result.get("memory_insights", {})
        }
        
        logger.info(f"Decision evaluated: {result.get('id')} - Risk: {result.get('risk_level')}")
        return response
        
    except KeyError as e:
        logger.error(f"Invalid category: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category. Must be one of: {', '.join([cat.name for cat in DecisionCategory])}"
        )
    except Exception as e:
        logger.error(f"Error evaluating decision: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error evaluating decision: {str(e)}"
        )


@app.post("/risk/assess", response_model=Dict[str, Any])
async def assess_risk(
    risk_request: RiskAssessmentRequest,
    api_info: Dict[str, Any] = Depends(verify_api_key)
):
    """
    Assess risk level for a decision or action
    
    - **amount**: Amount involved
    - **category**: Decision category
    - **description**: Description of the risk assessment
    """
    try:
        logger.info(f"Assessing risk: {risk_request.category} - ${risk_request.amount}")
        
        # Create decision data for risk assessment
        decision_data = {
            "amount": risk_request.amount,
            "category": risk_request.category,
            "description": risk_request.description
        }
        
        # Get memory insights for context
        memory_insights = decision_engine.memory.inform_decision(decision_data)
        
        # Assess risk
        risk_level = decision_engine._assess_risk(decision_data, memory_insights)
        
        # Get risk thresholds
        thresholds = decision_engine.risk_thresholds.get(risk_level, {})
        
        response = {
            "risk_level": risk_level.value,
            "risk_score": _calculate_risk_score(risk_level, risk_request.amount),
            "recommendation": _get_risk_recommendation(risk_level),
            "thresholds": {
                "max_amount": thresholds.get("max_amount"),
                "auto_execute": thresholds.get("auto_execute", False)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Risk assessed: {risk_level.value} - Score: {response['risk_score']}")
        return response
        
    except Exception as e:
        logger.error(f"Error assessing risk: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error assessing risk: {str(e)}"
        )


@app.get("/autonomy/level", response_model=Dict[str, Any])
async def get_autonomy_level(
    api_info: Dict[str, Any] = Depends(verify_api_key)
):
    """
    Get current AI autonomy level and system status
    
    Returns:
    - autonomy_level: Current autonomy percentage
    - target_autonomy: Target autonomy percentage
    - human_tasks: Remaining human tasks
    - ai_tasks: AI-managed tasks
    - proven_capabilities: List of proven AI capabilities
    """
    try:
        autonomy_system = decision_engine.autonomy
        tracker = autonomy_system.tracker
        
        status_data = tracker.get_autonomy_status()
        
        response = {
            "autonomy_level": status_data["current_autonomy"],
            "target_autonomy": status_data["target_autonomy"],
            "human_tasks": status_data["remaining_tasks"],
            "ai_tasks": status_data["ai_tasks"],
            "proven_capabilities": status_data["proven_capabilities"],
            "timestamp": datetime.now().isoformat()
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting autonomy level: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting autonomy level: {str(e)}"
        )


@app.post("/autonomy/should-execute", response_model=Dict[str, Any])
async def should_auto_execute(
    execute_request: AutoExecuteRequest,
    api_info: Dict[str, Any] = Depends(verify_api_key)
):
    """
    Determine if AI should autonomously execute a task
    
    - **task_type**: Type of task (e.g., "operational", "financial")
    - **risk_level**: Risk level (LOW, MEDIUM, HIGH, CRITICAL)
    """
    try:
        logger.info(f"Checking auto-execute: {execute_request.task_type} - {execute_request.risk_level}")
        
        should_execute = decision_engine.autonomy.should_auto_execute(
            execute_request.task_type, 
            execute_request.risk_level
        )
        
        response = {
            "should_execute": should_execute,
            "reason": _get_execution_reason(should_execute, execute_request.task_type, execute_request.risk_level),
            "task_type": execute_request.task_type,
            "risk_level": execute_request.risk_level,
            "timestamp": datetime.now().isoformat()
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error checking execution: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking execution: {str(e)}"
        )


@app.post("/memory/insights", response_model=Dict[str, Any])
async def get_memory_insights(
    insights_request: MemoryInsightsRequest,
    api_info: Dict[str, Any] = Depends(verify_api_key)
):
    """
    Get insights from AI memory system
    
    - **decision_data**: Decision data dictionary for context
    """
    try:
        logger.info("Fetching memory insights")
        
        decision_data = insights_request.decision_data
        
        insights = decision_engine.memory.inform_decision(decision_data)
        
        response = {
            "similar_decisions": len(insights.get("similar_decisions", [])) if isinstance(insights.get("similar_decisions"), list) else 0,
            "success_patterns": insights.get("success_patterns", {}),
            "recommendations": insights.get("recommendations", []) if isinstance(insights.get("recommendations"), list) else [],
            "timestamp": datetime.now().isoformat()
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting memory insights: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting memory insights: {str(e)}"
        )


# Helper methods
def _calculate_risk_score(risk_level, amount):
    """Calculate risk score 0-100"""
    base_scores = {
        RiskLevel.LOW: 25,
        RiskLevel.MEDIUM: 50,
        RiskLevel.HIGH: 75,
        RiskLevel.CRITICAL: 100
    }
    base_score = base_scores.get(risk_level, 50)
    
    # Adjust based on amount (higher amounts = higher risk)
    if amount > 100000:
        base_score += 10
    elif amount > 50000:
        base_score += 5
    
    return min(base_score, 100)


def _get_risk_recommendation(risk_level):
    """Get recommendation based on risk level"""
    recommendations = {
        RiskLevel.LOW: "Safe to proceed",
        RiskLevel.MEDIUM: "Proceed with caution",
        RiskLevel.HIGH: "Requires review",
        RiskLevel.CRITICAL: "Requires human approval"
    }
    return recommendations.get(risk_level, "Evaluate carefully")


def _get_execution_reason(should_execute, task_type, risk_level):
    """Get reason for execution decision"""
    if should_execute:
        return f"AI autonomy level sufficient for {risk_level} risk {task_type} tasks"
    else:
        return f"Insufficient autonomy level or task requires human oversight"


# Payment and Subscription Models
class CheckoutRequest(BaseModel):
    email: str = Field(..., description="Customer email address")
    tier: str = Field(default="pro", description="Subscription tier (pro, enterprise)")

class SubscriptionStatusResponse(BaseModel):
    subscription_id: Optional[str] = None
    status: str
    tier: str
    current_period_end: Optional[int] = None
    cancel_at_period_end: bool = False


# Payment and Subscription Endpoints
@app.post("/payment/checkout", response_model=Dict[str, Any])
async def create_checkout_session(checkout_request: CheckoutRequest):
    """
    Create Stripe checkout session for subscription
    
    - **email**: Customer email address
    - **tier**: Subscription tier (pro, enterprise)
    
    Returns checkout session URL
    """
    try:
        from api.stripe_service import stripe_service
        
        session = stripe_service.create_checkout_session(
            customer_email=checkout_request.email,
            tier=checkout_request.tier
        )
        
        return {
            "checkout_url": session["url"],
            "session_id": session["session_id"],
            "tier": session["tier"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating checkout session: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating checkout session: {str(e)}"
        )


@app.get("/payment/success")
async def payment_success(session_id: Optional[str] = None):
    """
    Payment success page - called after successful Stripe checkout
    """
    if not session_id:
        return {"message": "Payment successful! Check your email for API key."}
    
    try:
        from api.stripe_service import stripe_service, PRICING_TIERS
        from api.api_key_manager import api_key_manager
        import stripe
        
        # Retrieve checkout session
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.mode == "subscription" and session.subscription:
            # Get subscription details
            subscription = stripe_service.get_subscription(session.subscription)
            
            if subscription:
                tier = subscription.get("tier", "pro")
                customer_email = session.customer_email or session.metadata.get("customer_email", "")
                
                # Generate API key for this subscription
                api_key = api_key_manager.generate_api_key(tier=tier, prefix=f"{tier}_sub")
                
                # Link subscription to API key
                stripe_service.link_subscription_to_api_key(
                    api_key=api_key,
                    subscription_id=session.subscription,
                    customer_email=customer_email,
                    tier=tier
                )
                
                return {
                    "message": "Payment successful!",
                    "api_key": api_key,
                    "tier": tier,
                    "requests_per_month": PRICING_TIERS.get(tier, {}).get("requests_per_month", 0),
                    "subscription_id": session.subscription
                }
        
        return {"message": "Payment successful! Processing subscription..."}
    except Exception as e:
        logger.error(f"Error processing payment success: {e}", exc_info=True)
        return {"message": "Payment successful! We'll send your API key via email."}


@app.get("/payment/cancel")
async def payment_cancel():
    """Payment cancellation page"""
    return {"message": "Payment cancelled. You can try again anytime."}


@app.post("/webhooks/stripe", response_model=Dict[str, Any])
async def stripe_webhook(request: Request):
    """
    Handle Stripe webhook events
    
    Processes subscription updates, cancellations, etc.
    """
    try:
        from api.stripe_service import stripe_service
        from api.api_key_manager import api_key_manager
        
        payload = await request.body()
        signature = request.headers.get("stripe-signature")
        
        if not signature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing stripe-signature header"
            )
        
        # Verify webhook
        event = stripe_service.verify_webhook(payload, signature)
        
        if not event:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid webhook signature"
            )
        
        # Handle different event types
        event_type = event["type"]
        event_data = event["data"]["object"]
        
        if event_type == "checkout.session.completed":
            # Subscription created
            subscription_id = event_data.get("subscription")
            if subscription_id:
                subscription = stripe_service.get_subscription(subscription_id)
                if subscription:
                    tier = subscription.get("tier", "pro")
                    # Update subscription status
                    stripe_service.update_subscription_status(subscription_id, "active")
                    logger.info(f"Subscription activated: {subscription_id}")
        
        elif event_type == "customer.subscription.updated":
            # Subscription updated
            subscription_id = event_data.get("id")
            status = event_data.get("status")
            stripe_service.update_subscription_status(subscription_id, status)
            logger.info(f"Subscription updated: {subscription_id}, status: {status}")
        
        elif event_type == "customer.subscription.deleted":
            # Subscription cancelled
            subscription_id = event_data.get("id")
            stripe_service.update_subscription_status(subscription_id, "cancelled")
            
            # Optionally downgrade API key to free tier
            api_key = stripe_service.get_api_key_from_subscription(subscription_id)
            if api_key:
                keys = api_key_manager._load_keys()
                if api_key in keys:
                    keys[api_key]["tier"] = "free"
                    keys[api_key]["requests_per_month"] = 100
                    api_key_manager._save_keys(keys)
                    logger.info(f"Downgraded API key {api_key[:10]}... to free tier")
        
        return {"status": "success", "event": event_type}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing webhook: {str(e)}"
        )


@app.get("/subscription/status", response_model=SubscriptionStatusResponse)
async def get_subscription_status(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """
    Get subscription status for current API key
    """
    try:
        from api.stripe_service import stripe_service
        
        if not x_api_key:
            return SubscriptionStatusResponse(
                status="free",
                tier="free"
            )
        
        # Find subscription for this API key
        subscriptions = stripe_service._load_subscriptions()
        subscription_id = None
        
        for sub_id, sub_data in subscriptions.items():
            if sub_data.get("api_key") == x_api_key:
                subscription_id = sub_id
                break
        
        if not subscription_id:
            # Check tier from API key manager
            from api.api_key_manager import api_key_manager
            key_info = api_key_manager.validate_api_key(x_api_key)
            tier = key_info.get("tier", "free") if key_info else "free"
            
            return SubscriptionStatusResponse(
                status="free",
                tier=tier
            )
        
        subscription = stripe_service.get_subscription(subscription_id)
        if subscription:
            return SubscriptionStatusResponse(
                subscription_id=subscription["id"],
                status=subscription["status"],
                tier=subscription["tier"],
                current_period_end=subscription.get("current_period_end"),
                cancel_at_period_end=subscription.get("cancel_at_period_end", False)
            )
        
        # Fallback to API key tier
        from api.api_key_manager import api_key_manager
        key_info = api_key_manager.validate_api_key(x_api_key)
        tier = key_info.get("tier", "free") if key_info else "free"
        
        return SubscriptionStatusResponse(
            status="unknown",
            tier=tier
        )
    
    except Exception as e:
        logger.error(f"Error getting subscription status: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting subscription status: {str(e)}"
        )


@app.get("/pricing", response_model=Dict[str, Any])
async def get_pricing():
    """
    Get pricing information for all tiers
    """
    try:
        from api.stripe_service import PRICING_TIERS
        
        pricing = {}
        for tier, info in PRICING_TIERS.items():
            pricing[tier] = {
                "name": info["name"],
                "price": info["amount"] / 100,  # Convert cents to dollars
                "requests_per_month": info["requests_per_month"],
                "features": [
                    f"{info['requests_per_month']:,} requests/month",
                    "Full API access",
                    "Priority support" if tier != "free" else "Community support"
                ]
            }
        
        return {
            "tiers": pricing,
            "currency": "USD"
        }
    except Exception as e:
        logger.error(f"Error getting pricing: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting pricing: {str(e)}"
        )


# Include analytics routes
from api.analytics_routes import router as analytics_router
app.include_router(analytics_router)

# Include key management routes
from api.key_management_routes import router as key_management_router
app.include_router(key_management_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
