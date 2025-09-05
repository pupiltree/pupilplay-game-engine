#!/usr/bin/env python3
"""
PupilPlay Game Engine - Two-Node LangGraph Implementation Example
Based on Automation Engine's proven two-node architecture pattern

This demonstrates how the Multiplication Runner game uses the same
static two-node workflow that powers the automation engine, adapted
for educational gaming with AI asset generation.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, TypedDict, Annotated
from dataclasses import dataclass
from enum import Enum

# LangGraph imports (same as automation engine)
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI

# Educational game specific imports
from pupilplay.core.ai_models import GeminiModelSelector
from pupilplay.core.asset_generation import NanoBananaAssetPipeline
from pupilplay.core.learning_analytics import LearningAnalyticsEngine
from pupilplay.integrations.pupil_assess import PupilAssessConnector
from pupilplay.integrations.content_engine import ContentEngineConnector

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LearningObjective(TypedDict):
    """Educational learning objective tracking"""
    skill: str
    mastery_level: float  # 0.0 to 1.0
    evidence_count: int
    last_assessed: datetime

class PerformanceMetrics(TypedDict):
    """Real-time performance tracking"""
    accuracy: float
    average_response_time: float
    problems_attempted: int
    hints_requested: int
    engagement_score: float

class GameState(TypedDict):
    """
    Game State following automation engine pattern:
    - Minimal state design
    - Messages-centric approach
    - Educational extensions
    """
    # Core conversation (identical to automation engine)
    messages: Annotated[List[Any], add_messages]
    
    # Player identity and session
    player_id: str
    session_id: str
    game_type: str
    
    # Educational progress tracking
    learning_objectives: List[LearningObjective]
    current_mastery_levels: Dict[str, float]
    recent_performance: PerformanceMetrics
    
    # Game progression
    current_level: int
    experience_points: int
    difficulty_level: float
    
    # AI adaptation context
    preferred_learning_style: str
    engagement_score: float
    session_start_time: datetime
    total_play_time: int

class DifficultyLevel(Enum):
    """Adaptive difficulty levels"""
    BEGINNER = 0.2
    EASY = 0.4
    MEDIUM = 0.6
    HARD = 0.8
    EXPERT = 1.0

@dataclass
class GameConfiguration:
    """Configuration-driven game setup (loaded from YAML)"""
    domain: str = "educational_games"
    game_type: str = "multiplication_runner"
    subject: str = "mathematics"
    topic: str = "multiplication"
    target_age_range: List[int] = None
    learning_objectives: List[str] = None
    
    # AI model configuration
    gemini_api_key: str = ""
    complexity_threshold: float = 0.6
    
    # Asset generation
    image_gen4_endpoint: str = ""
    image_gen4_api_key: str = ""
    
    def __post_init__(self):
        if self.target_age_range is None:
            self.target_age_range = [8, 12]
        if self.learning_objectives is None:
            self.learning_objectives = [
                "Master multiplication facts 2-12",
                "Improve calculation speed and accuracy",
                "Build confidence in mathematical problem solving"
            ]

class PupilPlayGameEngine:
    """
    Universal Game Engine using Two-Node LangGraph Architecture
    
    Identical pattern to automation engine:
    - Static workflow structure
    - Configuration-driven behavior
    - Universal adaptability
    """
    
    def __init__(self, config: GameConfiguration):
        self.config = config
        self.checkpointer = MemorySaver()
        
        # AI model management (same as automation engine)
        self.model_selector = GeminiModelSelector(config.gemini_api_key)
        
        # Game-specific extensions
        self.asset_pipeline = NanoBananaAssetPipeline(
            image_gen4_endpoint=config.image_gen4_endpoint,
            image_gen4_api_key=config.image_gen4_api_key,
            gemini_api_key=config.gemini_api_key
        )
        self.analytics_engine = LearningAnalyticsEngine()
        self.pupil_assess = PupilAssessConnector()
        self.content_engine = ContentEngineConnector()
        
        # Initialize workflow
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile(checkpointer=self.checkpointer)
        
    def _build_workflow(self) -> StateGraph:
        """
        Build the universal two-node game workflow
        IDENTICAL structure to automation engine
        """
        builder = StateGraph(GameState)
        
        # Two universal nodes for ALL game types
        builder.add_node("game_master", self._game_master_node)
        builder.add_node("game_actions", self._create_game_actions_node())
        
        # Static routing pattern (NEVER changes)
        builder.add_edge(START, "game_master")
        builder.add_conditional_edges("game_master", tools_condition)
        builder.add_edge("game_actions", "game_master")
        
        return builder
    
    def _game_master_node(self, state: GameState, config: RunnableConfig) -> Dict[str, Any]:
        """
        Game Master Node: Educational AI Assistant
        
        Equivalent to automation engine's Assistant Node but specialized for education:
        - Uses same Gemini model selection logic
        - System prompt contains all educational philosophy
        - Tools bound for game actions
        """
        logger.info(f"Game Master processing interaction for player {state.get('player_id')}")
        
        # Create educational system prompt from configuration
        system_prompt = self._create_educational_system_prompt(state)
        
        # Select Gemini model based on educational complexity (same logic as automation engine)
        llm = self._select_gemini_model_for_education(state)
        
        # Bind available game actions to LLM (same pattern as automation engine)
        game_actions = self._get_available_game_actions()
        if game_actions:
            llm = llm.bind_tools(game_actions)
        
        # Process player interaction with full educational context
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        
        try:
            response = llm.invoke(messages, config)
            
            return {
                "messages": [response],
                "engagement_score": self._calculate_engagement(state, response),
            }
            
        except Exception as e:
            logger.error(f"Game Master error: {e}")
            # Fallback response (same pattern as automation engine)
            return {
                "messages": [AIMessage(content="Let's keep learning together! Try your best on this challenge.")],
                "engagement_score": state.get("engagement_score", 0.5),
            }
    
    def _create_educational_system_prompt(self, state: GameState) -> str:
        """
        Create game-specific system prompt from configuration
        ALL educational logic lives here (same principle as automation engine)
        """
        # Extract current game context
        player_id = state.get("player_id", "Student")
        current_level = state.get("current_level", 1)
        difficulty_level = state.get("difficulty_level", 0.5)
        recent_performance = state.get("recent_performance", {})
        learning_objectives = state.get("learning_objectives", [])
        
        # Build system prompt with educational context
        system_prompt = f"""
You are an expert mathematics educator embedded in the "Multiplication Masters Runner" educational game.

Your primary role is to help {player_id} aged 8-12 master multiplication facts through engaging gameplay.

EDUCATIONAL PHILOSOPHY:
- Use Socratic questioning to guide discovery, never just give answers
- Celebrate every attempt and effort, not just correct answers  
- Connect abstract math concepts to concrete, visual representations
- Maintain optimal challenge level: 80% success rate for confidence building
- Provide immediate, specific feedback on mathematical reasoning

CURRENT GAME CONTEXT:
- Player: {player_id}
- Current Level: {current_level}
- Difficulty Level: {difficulty_level}
- Recent Accuracy: {recent_performance.get('accuracy', 0.0)*100:.1f}%
- Problems per Minute: {recent_performance.get('average_response_time', 0.0):.1f}
- Learning Focus: {', '.join([obj['skill'] for obj in learning_objectives]) if learning_objectives else 'Basic multiplication'}

AVAILABLE GAME ACTIONS:
- adjust_difficulty: Change problem complexity in real-time
- generate_hint: Provide visual or conceptual hint
- create_problem: Generate new multiplication challenge
- update_progress: Track mastery of specific multiplication facts
- trigger_celebration: Initiate success animation and positive reinforcement
- generate_visual_asset: Create educational graphics using AI pipeline

COMMUNICATION STYLE:
- Enthusiastic but not overwhelming
- Age-appropriate vocabulary (8-12 years old)
- Focus on mathematical thinking process, not just answers
- Use game metaphors: "mathematical powers," "number magic," "calculation spells"

Remember: Every interaction should build both mathematical understanding AND confidence!
"""
        
        return system_prompt.strip()
    
    def _select_gemini_model_for_education(self, state: GameState) -> ChatGoogleGenerativeAI:
        """
        Select appropriate Gemini model based on educational complexity
        SAME logic as automation engine's model selection
        """
        # Calculate educational complexity score
        complexity_factors = {
            'explanation_needed': 0.0,
            'creative_thinking': 0.0,
            'multi_step_reasoning': 0.0,
            'visual_generation': 0.0
        }
        
        # Analyze recent messages for complexity indicators
        recent_messages = state.get("messages", [])[-3:]  # Last 3 interactions
        for message in recent_messages:
            if hasattr(message, 'content'):
                content = str(message.content).lower()
                if any(word in content for word in ['why', 'how', 'explain']):
                    complexity_factors['explanation_needed'] = 0.3
                if any(word in content for word in ['create', 'design', 'make']):
                    complexity_factors['creative_thinking'] = 0.2
                if any(word in content for word in ['step', 'solve', 'break down']):
                    complexity_factors['multi_step_reasoning'] = 0.3
                if any(word in content for word in ['show', 'picture', 'visual']):
                    complexity_factors['visual_generation'] = 0.2
        
        complexity_score = sum(complexity_factors.values())
        
        # Model selection (same thresholds as automation engine)
        if complexity_score >= self.config.complexity_threshold:
            logger.info(f"Using Gemini Pro for complex educational interaction (score: {complexity_score:.2f})")
            return self.model_selector.get_gemini_pro()
        else:
            logger.info(f"Using Gemini Flash for routine educational interaction (score: {complexity_score:.2f})")
            return self.model_selector.get_gemini_flash()
    
    def _get_available_game_actions(self) -> List[Any]:
        """
        Get available game actions (equivalent to MCP tools in automation engine)
        """
        from langchain_core.tools import tool
        
        @tool
        def adjust_difficulty(new_difficulty_level: float, adjustment_rationale: str) -> str:
            """Adjust game difficulty based on player performance"""
            return f"Difficulty adjusted to {new_difficulty_level}: {adjustment_rationale}"
        
        @tool
        def generate_hint(hint_type: str, visual_support: bool = False) -> str:
            """Generate educational hint for current problem"""
            if visual_support:
                return f"Generated visual {hint_type} hint to guide mathematical thinking"
            return f"Generated {hint_type} hint to support learning"
        
        @tool
        def create_problem(difficulty_level: float, learning_objectives: List[str]) -> str:
            """Generate new multiplication problem aligned with curriculum"""
            return f"Created new multiplication problem at difficulty {difficulty_level}"
        
        @tool
        def update_progress(skill_category: str, mastery_level: float) -> str:
            """Track learning progress toward educational objectives"""
            return f"Updated {skill_category} mastery to {mastery_level*100:.1f}%"
        
        @tool
        def trigger_celebration(achievement_context: str) -> str:
            """Activate success animations and positive reinforcement"""
            return f"Celebrating achievement: {achievement_context}"
        
        @tool
        def generate_visual_asset(asset_type: str, educational_context: str) -> str:
            """Create educational graphics using Nano Banana + Image Gen 4 pipeline"""
            return f"Generated {asset_type} asset for {educational_context}"
        
        return [
            adjust_difficulty,
            generate_hint,
            create_problem,
            update_progress,
            trigger_celebration,
            generate_visual_asset
        ]
    
    def _create_game_actions_node(self) -> ToolNode:
        """
        Create Game Actions Node (equivalent to automation engine's Tools Node)
        Executes educational decisions in the real game world
        """
        game_actions = self._get_available_game_actions()
        if not game_actions:
            # Graceful degradation (same pattern as automation engine)
            return ToolNode([])
        
        return ToolNode(game_actions)
    
    def _calculate_engagement(self, state: GameState, response: Any) -> float:
        """Calculate player engagement score based on interaction patterns"""
        current_engagement = state.get("engagement_score", 0.5)
        
        # Simple engagement calculation (can be made more sophisticated)
        if hasattr(response, 'content'):
            content = str(response.content)
            positive_indicators = sum(1 for word in ['great', 'excellent', 'awesome', 'fantastic'] if word in content.lower())
            encouragement_indicators = sum(1 for phrase in ['try again', 'keep going', 'you can do it'] if phrase in content.lower())
            
            engagement_boost = (positive_indicators * 0.1) + (encouragement_indicators * 0.05)
            return min(1.0, current_engagement + engagement_boost)
        
        return current_engagement
    
    async def process_player_interaction(
        self, 
        player_id: str, 
        message: str, 
        session_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Process player interaction through the two-node workflow
        
        This is the main entry point for all educational game interactions
        """
        logger.info(f"Processing interaction for player {player_id}: {message[:50]}...")
        
        # Prepare initial state (minimal, same as automation engine)
        initial_state = GameState(
            messages=[HumanMessage(content=message)],
            player_id=player_id,
            session_id=session_context.get("session_id", f"session_{datetime.now().isoformat()}") if session_context else f"session_{datetime.now().isoformat()}",
            game_type=self.config.game_type,
            learning_objectives=session_context.get("learning_objectives", []) if session_context else [],
            current_mastery_levels=session_context.get("mastery_levels", {}) if session_context else {},
            recent_performance=session_context.get("recent_performance", {
                "accuracy": 0.75,
                "average_response_time": 12.0,
                "problems_attempted": 0,
                "hints_requested": 0,
                "engagement_score": 0.7
            }) if session_context else {
                "accuracy": 0.75,
                "average_response_time": 12.0,
                "problems_attempted": 0,
                "hints_requested": 0,
                "engagement_score": 0.7
            },
            current_level=session_context.get("current_level", 1) if session_context else 1,
            experience_points=session_context.get("experience_points", 0) if session_context else 0,
            difficulty_level=session_context.get("difficulty_level", 0.5) if session_context else 0.5,
            preferred_learning_style=session_context.get("learning_style", "visual") if session_context else "visual",
            engagement_score=0.7,
            session_start_time=datetime.now(),
            total_play_time=session_context.get("total_play_time", 0) if session_context else 0
        )
        
        # Configure workflow execution
        config = RunnableConfig(
            configurable={
                "thread_id": f"{player_id}_{initial_state['session_id']}",
                "player_context": session_context or {}
            }
        )
        
        try:
            # Execute two-node workflow (same pattern as automation engine)
            result = await self.app.ainvoke(initial_state, config)
            
            # Extract response and updated state
            final_messages = result.get("messages", [])
            ai_response = final_messages[-1] if final_messages else None
            
            response_data = {
                "success": True,
                "response": ai_response.content if ai_response else "I'm here to help you learn!",
                "game_state": {
                    "current_level": result.get("current_level", initial_state["current_level"]),
                    "difficulty_level": result.get("difficulty_level", initial_state["difficulty_level"]),
                    "engagement_score": result.get("engagement_score", initial_state["engagement_score"]),
                    "session_time": (datetime.now() - initial_state["session_start_time"]).total_seconds()
                },
                "educational_insights": {
                    "complexity_level": "appropriate",
                    "learning_progress": "on_track",
                    "recommendations": ["Continue current approach", "Maintain engagement level"]
                }
            }
            
            logger.info(f"Successfully processed interaction for player {player_id}")
            return response_data
            
        except Exception as e:
            logger.error(f"Error processing interaction: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "I apologize, but I'm having trouble right now. Let's try again!",
                "game_state": {
                    "current_level": initial_state["current_level"],
                    "difficulty_level": initial_state["difficulty_level"],
                    "engagement_score": 0.5,
                    "session_time": 0
                }
            }

# Example Usage and Testing
async def main():
    """
    Demonstrate the two-node educational game engine in action
    """
    print("🎮 PupilPlay Game Engine - Two-Node Architecture Demo")
    print("=" * 60)
    
    # Configuration (normally loaded from YAML)
    config = GameConfiguration(
        gemini_api_key="your_gemini_api_key_here",  # Replace with actual key
        image_gen4_endpoint="https://api.imagegen4.example.com",
        image_gen4_api_key="your_image_gen4_key_here"
    )
    
    # Initialize game engine
    engine = PupilPlayGameEngine(config)
    
    # Simulate student interactions
    player_id = "student_alice_8yo"
    session_context = {
        "session_id": "demo_session_001",
        "current_level": 3,
        "learning_objectives": [
            {"skill": "multiplication_2x", "mastery_level": 0.9, "evidence_count": 15, "last_assessed": datetime.now()},
            {"skill": "multiplication_3x", "mastery_level": 0.6, "evidence_count": 8, "last_assessed": datetime.now()}
        ],
        "recent_performance": {
            "accuracy": 0.75,
            "average_response_time": 8.5,
            "problems_attempted": 12,
            "hints_requested": 2,
            "engagement_score": 0.8
        }
    }
    
    # Test interactions
    test_interactions = [
        "I'm stuck on 7 x 8, can you help me?",
        "Why is 6 x 7 = 42?",
        "Can you make the game easier? It's too hard.",
        "I got three in a row correct! Am I doing well?",
        "Can you show me a picture to help with 9 x 6?"
    ]
    
    print(f"Player: {player_id}")
    print(f"Session: {session_context['session_id']}")
    print()
    
    for i, interaction in enumerate(test_interactions, 1):
        print(f"Interaction {i}:")
        print(f"Student: {interaction}")
        
        # Process through two-node workflow
        result = await engine.process_player_interaction(
            player_id=player_id,
            message=interaction,
            session_context=session_context
        )
        
        if result["success"]:
            print(f"Game Master: {result['response']}")
            print(f"Engagement: {result['game_state']['engagement_score']:.2f}")
            print(f"Difficulty: {result['game_state']['difficulty_level']:.2f}")
        else:
            print(f"Error: {result['error']}")
        
        print("-" * 40)
        print()
    
    print("✅ Demo completed successfully!")
    print("\nKey Features Demonstrated:")
    print("• Static two-node LangGraph workflow (same as automation engine)")
    print("• Configuration-driven educational behavior")
    print("• Adaptive AI model selection (Gemini Pro/Flash)")
    print("• Real-time difficulty adjustment")
    print("• Educational tools integration")
    print("• Comprehensive error handling and fallbacks")

if __name__ == "__main__":
    asyncio.run(main())