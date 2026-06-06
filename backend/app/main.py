import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.ai.ai_provider_manager import AIProviderManager
from app.memory.continuity_memory_service import ContinuityMemoryService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.db import init_db
init_db()

ai_provider = AIProviderManager()
continuity_memory = ContinuityMemoryService()


@app.get("/")
def root():
    return {"message": "Cyris AI Assistant backend is running"}


class PromptRequest(BaseModel):
    prompt: str


@app.post("/ai-test")
def ai_test(
        request: PromptRequest
):
    response = (
        ai_provider.generate_ai_response(
            request.prompt,
            add_to_history=False
        )
    )

    return {
        "response": (
            response["response"]
        ),

        "summary": (
            response["summary"]
        )
    }


@app.post("/chat")
def chat(request: PromptRequest):
    ai_response = (
        ai_provider.generate_ai_response(
            request.prompt
        )
    )

    if isinstance(ai_response, dict):

        content = (
                ai_response.get("response")
                or ai_response.get("content")
        )

        if isinstance(content, dict):
            content = (
                    content.get("response")
                    or content.get("content")
            )

    else:

        content = ai_response

    return {
        "response": str(content),
        "session_id": "default-session"
    }


@app.get("/session-start")
def session_start():
    from app.memory.conversation_history_service import ConversationHistoryService
    history_service = ConversationHistoryService()

    continuity = (
        continuity_memory
        .load_memory()
    )

    items = [item for item in continuity.get("continuity_items", []) if not item.get("retired", False)]

    if not items:
        default_greeting = (
            "Hello. I'm Cyris. "
            "Tell me a little about yourself "
            "and what matters to you right now."
        )
        history_service.save_history({"messages": []})
        history_service.add_message("assistant", default_greeting)
        return {
            "message": default_greeting
        }

    # Generate a dynamic greeting using the active AI provider based on continuity context
    formatted_items = []
    for item in items:
        formatted_items.append(f"- {item.get('content')} ({item.get('type')})")
    items_str = "\n".join(formatted_items)

    prompt = f"""
    You are Cyris, a calm, intelligent, and context-aware AI assistant.
    The user is starting a new session. Generate a brief, warm, and natural welcome-back greeting.
    Reference 1 or 2 of their active continuity areas naturally so they feel you remember them, but keep it calm, light, and concise (1-2 sentences). Do not use robotic phrasing like "Welcome back! I see you are..." or be overly enthusiastic.
    
    CRITICAL: Strictly output ONLY the greeting text itself. Do not include any reasoning, chain-of-thought, self-corrections, planning, or headers in your output.
    
    Active continuity profile:
    {items_str}
    
    Greeting:
    """

    try:
        response = ai_provider.generate_ai_response(prompt, add_to_history=False)
        if isinstance(response, dict):
            greeting = response.get("response") or response.get("content") or str(response)
            if isinstance(greeting, dict):
                greeting = greeting.get("response") or greeting.get("content") or str(greeting)
        else:
            greeting = str(response)

        greeting = greeting.strip().strip('"').strip("'")
    except Exception:
        # Fallback to template if LLM call fails
        latest = items[-1]
        content = latest.get("content", "something important")
        greeting = f"Welcome back. Last time we were discussing {content}. Would you like to continue from there?"

    # Reset history for the new session and append the greeting
    history_service.save_history({"messages": []})
    history_service.add_message("assistant", greeting)

    return {
        "message": greeting
    }



@app.get("/memory-status")
def memory_status():
    memory = (
        continuity_memory
        .load_memory()
    )

    return {
        "continuity_items":
            memory.get(
                "continuity_items",
                []
            )
    }


@app.delete("/memory/{identity}")
def delete_memory_item(identity: str):
    success = continuity_memory.delete_continuity_item(identity)
    if success:
        return {"status": "success", "message": f"Memory item '{identity}' deleted."}
    else:
        return {"status": "error", "message": "Failed to delete memory item."}


@app.post("/memory/reconcile")
def reconcile_memory():
    try:
        from app.memory.memory_reconciler import MemoryReconciler
        reconciler = MemoryReconciler()
        result = reconciler.rebuild_memory_from_history(ai_provider)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}



# @app.get("/guidance")
# def guidance():
#     sample_user = UserProfile(
#         name="Aman",
#         long_term_goals=[
#             "Become financially independent through technology"
#         ],
#         active_focus_areas=[
#             "Web Development",
#             "Cybersecurity"
#         ]
#     )
#
#     sample_context = ContextState(
#         energy_level="low",
#         current_priority="Web Development"
#     )
#
#     sample_priorities = PriorityState(
#         high_priority=["Web Development"]
#     )
#
#     result = assistant.generate_guidance(
#         user=sample_user,
#         context=sample_context,
#         priorities=sample_priorities
#     )
#
#     return {
#         "guidance": result
#     }


# @app.get("/behavior")
# def behavior():
#
#     sample_event = BehaviorEvent(
#         event_type="inactivity",
#         focus_area="Web Development",
#         engagement_level=2,
#         notes="No progress reported for several days"
#     )
#
#     result = behavior_tracker.analyze_behavior(
#         event=sample_event
#     )
#
#     return result


# @app.get("/memory")
# def memory():
#     sample_user = UserProfile(
#         name="Aman",
#         long_term_goals=[
#             "Build adaptive AI systems"
#         ],
#         active_focus_areas=[
#             "Backend Development",
#             "Behavioral Intelligence"
#         ]
#     )
#
#     save_result = memory_manager.save_user_profile(
#         sample_user
#     )
#
#     retrieved_user = memory_manager.get_user_profile(
#         "Aman"
#     )
#
#     return {
#         "save_status": save_result,
#         "retrieved_user": retrieved_user
#     }


# @app.get("/context")
# def context():
#     sample_context = ContextState(
#         workload_level="high",
#         energy_level="low",
#         available_time="medium"
#     )
#
#     result = context_manager.evaluate_context(
#         sample_context
#     )
#
#     return result


# @app.get("/priority")
# def priority():
#     sample_priorities = PriorityState(
#         high_priority=["Web Development"],
#         medium_priority=["Cybersecurity"],
#         low_priority=["Blender"]
#     )
#
#     behavior_result = behavior_tracker.analyze_behavior(
#         BehaviorEvent(
#             event_type="inactivity"
#         )
#     )
#
#     context_result = context_manager.evaluate_context(
#         ContextState(
#             workload_level="high"
#         )
#     )
#
#     result = priority_engine.adjust_priorities(
#         priorities=sample_priorities,
#         behavior_signal=behavior_result["priority_adjustment"],
#         context_mode=context_result["mode"]
#     )
#
#     return result


# @app.get("/state")
# def state():
#     state_service.record_behavior(
#         "Repeated inactivity detected"
#     )
#
#     state_service.record_context_change(
#         "High workload period"
#     )
#
#     state_service.record_priority_change(
#         "Reduced complexity mode activated"
#     )
#
#     history = state_service.get_state_history()
#
#     return history


# @app.get("/adaptive-session")
# def adaptive_session():
#     result = adaptive_session_service.run_adaptive_session()
#
#     return result


# @app.get("/lifecycle")
# def lifecycle():
#     result = lifecycle_service.evaluate_lifecycle_state(
#         inactivity_days=6,
#         focus_area="Backend Development"
#     )
#
#     return result


# @app.get("/patterns")
# def patterns():
#     result = pattern_analysis_service.analyze_patterns(
#         inactivity_events=4,
#         overload_events=2,
#         focus_switches=5
#     )
#
#     return result


# @app.get("/intervention")
# def intervention():
#     lifecycle_result = lifecycle_service.evaluate_lifecycle_state(
#         inactivity_days=8,
#         focus_area="Backend Development"
#     )
#
#     pattern_result = pattern_analysis_service.analyze_patterns(
#         inactivity_events=4,
#         overload_events=2,
#         focus_switches=5
#     )
#
#     result = intervention_service.evaluate_intervention(
#         lifecycle_stage=lifecycle_result.current_stage,
#         detected_patterns=pattern_result["detected_patterns"]
#     )
#
#     return result


# @app.get("/focus")
# def focus():
#     result = focus_orchestrator_service.orchestrate_focus(
#         career_urgency="high",
#         energy_level="low",
#         active_focus_areas=[
#             "Backend Development",
#             "Cybersecurity",
#             "Blender",
#             "UI Design"
#         ]
#     )
#
#     return result


# @app.get("/recommendation")
# def recommendation():
#     focus_result = focus_orchestrator_service.orchestrate_focus(
#         career_urgency="high",
#         energy_level="low",
#         active_focus_areas=[
#             "Backend Development",
#             "Cybersecurity",
#             "Blender"
#         ]
#     )
#
#     primary_focus = focus_result["primary_focus"]
#
#     if isinstance(primary_focus, list):
#         selected_focus = primary_focus[0]
#     else:
#         selected_focus = primary_focus
#
#     result = recommendation_service.generate_recommendation(
#         focus_area=selected_focus,
#         energy_level="low",
#         available_time="short"
#     )
#
#     return result


# @app.get("/session-continuity")
# def session_continuity():
#     recommendation_result = recommendation_service.generate_recommendation(
#         focus_area="Backend Development",
#         energy_level="low",
#         available_time="short"
#     )
#
#     session_continuity_service.update_session(
#         focus_area="Backend Development",
#         recommendation=recommendation_result["action"],
#         continuity_change=1,
#         status="recovering"
#     )
#
#     return session_continuity_service.get_session_state()


# @app.get("/memory-classification")
# def memory_classification():
#     result = memory_classification_service.classify_memory(
#         identity_traits=[
#             "Strong interest in adaptive AI systems",
#             "Values long-term growth"
#         ],
#         temporary_states=[
#             "Currently experiencing workload pressure"
#         ],
#         patterns=[
#             "Recurring disengagement during overload periods"
#         ],
#         priorities=[
#             "Backend Development",
#             "Behavioral Intelligence"
#         ]
#     )
#
#     return result


# @app.get("/adaptive-guidance")
# def adaptive_guidance():
#     memory_result = memory_classification_service.classify_memory(
#         identity_traits=[
#             "Strong interest in adaptive AI systems",
#             "Values long-term growth"
#         ],
#         temporary_states=[
#             "Currently experiencing workload pressure"
#         ],
#         patterns=[
#             "Recurring disengagement during overload periods"
#         ],
#         priorities=[
#             "Backend Development",
#             "Behavioral Intelligence"
#         ]
#     )
#
#     result = adaptive_guidance_engine.generate_adaptive_guidance(
#         persistent_identity=memory_result.persistent_identity,
#         behavioral_patterns=memory_result.behavioral_patterns,
#         adaptive_priorities=memory_result.adaptive_priorities,
#         energy_level="low"
#     )
#
#     return result


# @app.get("/proactive-awareness")
# def proactive_awareness():
#     result = proactive_awareness_service.evaluate_proactive_state(
#         continuity_score=3,
#         inactivity_days=8,
#         overload_detected=True
#     )
#
#     return result


# @app.get("/strategy")
# def strategy():
#     result = strategic_planning_service.generate_strategy(
#         career_pressure="high",
#         burnout_risk="high",
#         active_focus_areas=[
#             "Backend Development",
#             "Behavioral Intelligence",
#             "Cybersecurity",
#             "UI Design"
#         ]
#     )
#
#     return result


# @app.get("/reflection")
# def reflection():
#     result = reflection_service.evaluate_guidance_effectiveness(
#         recommendation_followed=False,
#         continuity_change=-1,
#         overload_detected=True
#     )
#
#     return result


# @app.get("/alignment")
# def alignment():
#     result = alignment_engine.evaluate_alignment(
#         long_term_goal="Backend Development",
#         current_focus=[
#             "Backend Development",
#             "Cybersecurity",
#             "UI Design",
#             "Blender"
#         ],
#         fragmentation_level="high"
#     )
#
#     return result


# @app.get("/decision")
# def decision():
#     result = decision_synthesis_service.synthesize_direction(
#         lifecycle_stage="drifting",
#         overload_detected=True,
#         alignment_status="aligned",
#         continuity_score=2
#     )
#
#     return result


# @app.get("/forecast")
# def forecast():
#     result = forecasting_service.evaluate_risk_forecast(
#         continuity_score=2,
#         overload_detected=True,
#         fragmentation_level="high",
#         inactivity_days=6
#     )
#
#     return result


# @app.get("/recovery")
# def recovery():
#     result = recovery_service.generate_recovery_strategy(
#         forecast="high_drift_risk",
#         overload_detected=True,
#         continuity_score=1
#     )
#
#     return result


# @app.get("/adaptive-coordination")
# def adaptive_coordination():
#     result = (
#         adaptive_coordination_service
#         .coordinate_adaptive_response()
#     )
#
#     return result


# @app.get("/stability")
# def stability():
#     result = stability_service.calculate_stability(
#         continuity_score=3,
#         overload_detected=True,
#         inactivity_days=6,
#         fragmentation_level="high"
#     )
#
#     return result


# @app.get("/focus-state")
# def focus_state():
#     stability_result = stability_service.calculate_stability(
#         continuity_score=2,
#         overload_detected=True,
#         inactivity_days=6,
#         fragmentation_level="high"
#     )
#
#     result = focus_state_service.evaluate_focus_transition(
#         stability_state=stability_result["stability_state"],
#         continuity_score=2,
#         overload_detected=True
#     )
#
#     return result


# @app.get("/priority-cycle")
# def priority_cycle():
#     result = priority_cycle_service.cycle_priorities(
#         active_priorities=[
#             "Backend Development",
#             "Cybersecurity",
#             "UI Design",
#             "Blender"
#         ],
#         overload_detected=True,
#         continuity_score=2
#     )
#
#     return result


# @app.get("/continuity-escalation")
# def continuity_escalation():
#     result = continuity_escalation_service.evaluate_escalation(
#         continuity_score=1,
#         inactivity_days=8,
#         overload_detected=True
#     )
#
#     return result


# @app.get("/behavioral-orchestrator")
# def behavioral_orchestrator():
#     result = (
#         behavioral_orchestrator_service
#         .orchestrate_behavioral_state()
#     )
#
#     return result


# @app.get("/event")
# def event():
#     result = event_service.create_event(
#         event_type="continuity_decline",
#         description=(
#             "User inactivity exceeded expected continuity threshold."
#         ),
#         severity="moderate"
#     )
#
#     return result


# @app.get("/event-pipeline")
# def event_pipeline():
#     result = (
#         event_pipeline_service.process_event(
#             event_type="continuity_decline"
#         )
#     )
#
#     return result


# @app.get("/system-state")
# def system_state():
#     state_engine_service.update_state(
#         continuity_score=2,
#         overload_detected=True,
#         fragmentation_level="high",
#         inactivity_days=7,
#         focus_state="stabilization",
#         escalation_level="moderate"
#     )
#
#     return state_engine_service.get_state()


# @app.get("/execution-cycle")
# def execution_cycle():
#     result = (
#         execution_engine_service
#         .execute_runtime_cycle()
#     )
#
#     return result


# @app.get("/runtime-scheduler")
# def runtime_scheduler():
#     result = (
#         runtime_scheduler_service
#         .schedule_runtime_cycle()
#     )
#
#     return result


# @app.get("/runtime-loop")
# def runtime_loop():
#     result = (
#         runtime_loop_service.execute_loop(
#             cycles=3
#         )
#     )
#
#     return result


# @app.get("/system-status")
# def system_status():
#     return (
#         startup_validator
#         .validate_environment()
#     )


# @app.get("/validation-summary")
# def validation_summary():
#     return (
#         validation_summary_service
#         .generate_summary()
#     )
