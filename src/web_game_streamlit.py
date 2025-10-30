import streamlit as st
import json
import os
import random
from datetime import datetime
import time
from types import ModuleType
from typing import Optional

# Try to import python-vlc. If import fails we keep `vlc` as None and set a
# flag so code that depends on it can be skipped. We avoid giving the type
# checker an ambiguous variable by annotating `vlc`.
try:
    import vlc  # type: ignore
    HAS_VLC = True
except Exception:
    vlc: Optional[ModuleType] = None  # type: ignore
    HAS_VLC = False

def load_questions():
    """Load questions from the JSON file."""
    questions_file = os.path.join(os.path.dirname(__file__), '../assets/questions.json')
    with open(questions_file, 'r') as f:
        return json.load(f)

class HalloweenQuizStreamlit:
    def __init__(self):
        self.questions = load_questions()
        self.categories = {
            'spooky': 'Spooky Stories and Urban Legends',
            'costumes': 'Halloween Costumes and Traditions',
            'movies': 'Horror Movies and Characters',
            'history': 'Halloween History and Facts',
            'candy': 'Halloween Candy and Treats',
            'paranormal': 'Paranormal Activity'
        }
        # Initialize VLC instance for sound if available
        self.sound_players = {}
        self.vlc_instance = None
        if HAS_VLC:
            try:
                # Narrow type for the checker and guard at runtime in case the
                # imported `vlc` module is unusable (missing libvlc runtime).
                assert 'vlc' in globals() and vlc is not None
                self.vlc_instance = vlc.Instance()
                if self.vlc_instance is None:
                    # vlc.Instance() failed to initialize properly
                    raise RuntimeError("vlc.Instance() returned None")
                self._init_sounds()
            except Exception:
                # libVLC is not available or failed to initialize; disable sound
                self.vlc_instance = None
                self.sound_players = {}
    
    def _init_sounds(self):
        """Initialize sound players."""
        sound_dir = os.path.join(os.path.dirname(__file__), '../assets/sounds')
        # include start and congrats so they can be played when appropriate
        for sound_type in ['correct', 'incorrect', 'background', 'start', 'congrats']:
            # prefer mp3, fall back to wav
            sound_file = None
            for ext in ('.mp3', '.wav'):
                candidate = os.path.join(sound_dir, f'{sound_type}{ext}')
                if os.path.exists(candidate):
                    sound_file = candidate
                    break
            if not sound_file:
                continue
                # Guard against self.vlc_instance being None (defensive)
                if self.vlc_instance is None:
                    continue
                # Some libVLC bindings may return None from these factory
                # methods if the runtime is missing; guard against that.
                try:
                    media = self.vlc_instance.media_new(sound_file)
                    player = self.vlc_instance.media_player_new()
                    if player is None:
                        continue
                    if media is not None:
                        player.set_media(media)
                    self.sound_players[sound_type] = player
                except Exception:
                    # If any call into libVLC fails, skip this sound
                    continue

    def start_background(self):
        """Start background music if available."""
        player = self.sound_players.get('background')
        if player is None:
            return
        try:
            # many VLC backends will honor play() and use the media's loop
            player.play()
        except Exception:
            pass

    def stop_background(self):
        """Stop background music if playing."""
        player = self.sound_players.get('background')
        if player is None:
            return
        try:
            player.stop()
        except Exception:
            pass
    
    def play_sound(self, sound_type):
        """Play a sound effect."""
        # Defensive: ensure VLC is available and a player exists for the
        # requested sound. If not, do nothing.
        if not HAS_VLC or not self.sound_players:
            return
        player = self.sound_players.get(sound_type)
        if player is None:
            return
        try:
            # Some player implementations may be None or may raise; guard
            # against both to avoid crashing the Streamlit app.
            if hasattr(player, 'stop'):
                player.stop()
            if hasattr(player, 'play'):
                player.play()
        except Exception:
            # ignore playback errors in Streamlit UI
            pass
    
    def get_questions(self, selected_categories, difficulty):
        """Get questions from selected categories based on difficulty."""
        all_questions = []
        for category in selected_categories:
            if category in self.questions:
                questions = [q for q in self.questions[category] 
                           if q.get('difficulty', 'medium') == difficulty]
                all_questions.extend(questions)
        
        if not all_questions:  # Fallback if no questions for selected difficulty
            for category in selected_categories:
                if category in self.questions:
                    all_questions.extend(self.questions[category])
        
        random.shuffle(all_questions)
        return all_questions[:10]  # 10 questions per game

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'timer' not in st.session_state:
        st.session_state.timer = 30
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'quiz' not in st.session_state:
        st.session_state.quiz = HalloweenQuizStreamlit()

def display_halloween_header():
    """Display the Halloween-themed header."""
    st.markdown("""
    <style>
    .big-font {
        font-size: 50px !important;
        font-weight: bold;
        color: #ff6b00;
        text-align: center;
        margin-bottom: 20px;
    }
    .score-font {
        font-size: 24px;
        color: #ff6b00;
        text-align: center;
    }
    .timer {
        font-size: 48px;
        font-weight: bold;
        color: #ff4b4b;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .stButton>button {
        background-color: #333;
        color: #ff9933;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #444;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="big-font">🎃 Halloween Quiz 🎃</p>', unsafe_allow_html=True)
    
    st.text("""
     ____                        
    |    |                     
   /     \\                    
  |  O  O  |                   
  |   ^    |                   
   \\  --  /                    
    `----`                     
    """)

def display_timer():
    """Display and update the countdown timer (non-blocking).

    This implementation avoids a long blocking while-loop. It tracks the last
    tick time in session state, decrements the remaining timer by elapsed
    seconds, updates the UI, and triggers a lightweight rerun to continue the
    countdown. When the timer reaches zero the function returns True.
    """
    if 'time_remaining' not in st.session_state:
        st.session_state.time_remaining = 30
        st.session_state._timer_last = time.time()

    now = time.time()
    elapsed = int(now - st.session_state.get('_timer_last', now))
    if elapsed >= 1 and st.session_state.time_remaining > 0:
        st.session_state.time_remaining = max(0, st.session_state.time_remaining - elapsed)
        st.session_state._timer_last = now
        # If there's still time left, request a rerun so the UI updates again in ~1s
        if st.session_state.time_remaining > 0:
            st.rerun()

    time_placeholder = st.empty()
    progress_placeholder = st.empty()
    time_placeholder.markdown(f'<p class="timer">{st.session_state.time_remaining}</p>', unsafe_allow_html=True)
    progress = st.session_state.time_remaining / 30 if 30 else 0
    progress_placeholder.progress(progress)

    return st.session_state.time_remaining == 0

def save_high_score():
    """Save the player's score to the high scores file."""
    score_file = os.path.join(os.path.dirname(__file__), '../high_scores.csv')
    with open(score_file, 'a') as f:
        f.write(f"{st.session_state.player_name},{st.session_state.score},"
                f"{datetime.now()},{st.session_state.difficulty}\n")

def main():
    st.set_page_config(page_title="Halloween Quiz 🎃", page_icon="🎃", layout="centered")
    initialize_session_state()
    display_halloween_header()
    # Show audio players as controls (fallback) so users can manually play
    # background/start/congrats sounds if client-side playback is desired.
    sounds_dir = os.path.join(os.path.dirname(__file__), '../assets/sounds')
    try:
        def pick(name):
            for ext in ('.mp3', '.wav'):
                p = os.path.join(sounds_dir, f"{name}{ext}")
                if os.path.exists(p):
                    return p
            return None

        bg = pick('background')
        if bg and st.session_state.get('game_started', False):
            with open(bg, 'rb') as f:
                st.audio(f.read(), format='audio/wav' if bg.endswith('.wav') else 'audio/mp3')
        # Also show start/congrats players so users can manually trigger them
        st_file = pick('start')
        if st_file and not st.session_state.get('game_started', False):
            with open(st_file, 'rb') as f:
                st.audio(f.read(), format='audio/wav' if st_file.endswith('.wav') else 'audio/mp3')
        cong = pick('congrats')
        if cong and st.session_state.get('game_over', False):
            with open(cong, 'rb') as f:
                st.audio(f.read(), format='audio/wav' if cong.endswith('.wav') else 'audio/mp3')
    except Exception:
        # If file read or st.audio fails, silently continue — server-side VLC
        # playback is the preferred/primary mechanism.
        pass
    
    if not st.session_state.game_started:
        # Game setup
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("### Welcome to the Halloween Quiz! 👻")
            player_name = st.text_input("Enter your name, brave soul:", 
                                      placeholder="Your spooky name")
            difficulty = st.selectbox("Choose your difficulty:", 
                                    ['easy', 'medium', 'hard'])
            
            st.write("### Select Categories:")
            selected_categories = []
            for cat_id, cat_name in st.session_state.quiz.categories.items():
                if st.checkbox(cat_name, value=True, key=cat_id):
                    selected_categories.append(cat_id)

            # Start button should be shown once (outside the category loop)
            if st.button("Start Game") and player_name and selected_categories:
                st.session_state.game_started = True
                st.session_state.player_name = player_name
                st.session_state.difficulty = difficulty
                st.session_state.questions = st.session_state.quiz.get_questions(
                    selected_categories, difficulty)
                # Play start sound (server-side via VLC if available)
                try:
                    st.session_state.quiz.play_sound('start')
                except Exception:
                    pass
                # Start background music if available (server-side)
                try:
                    st.session_state.quiz.start_background()
                except Exception:
                    pass
                st.rerun()
    
    elif st.session_state.game_over:
        st.markdown(f'<p class="score-font">Final Score: {st.session_state.score}</p>', 
                   unsafe_allow_html=True)
        if st.button("Play Again"):
            st.session_state.clear()
            st.rerun()
    
    else:
        # Display score
        st.markdown(f'<p class="score-font">Score: {st.session_state.score}</p>', 
                   unsafe_allow_html=True)
        
        # Get current question
        current_q = st.session_state.questions[st.session_state.current_question]
        
        # Display question
        st.write(f"### {current_q['question']}")
        
        # Create columns for timer and options
        col1, col2 = st.columns([1, 2])
        
        with col1:
            time_up = display_timer()
        
        with col2:
            # Display options as buttons
            for i, option in enumerate(current_q['options']):
                if st.button(option, key=f"opt_{i}"):
                    # Check answer
                    correct_answer = current_q['options'].index(current_q['correct_answer'])
                    if i == correct_answer:
                        points = {'easy': 1, 'medium': 2, 'hard': 3}
                        st.session_state.score += points.get(st.session_state.difficulty, 1)
                        st.session_state.quiz.play_sound('correct')
                        st.success("✨ Correct! You're scarily good at this!")
                    else:
                        st.session_state.quiz.play_sound('incorrect')
                        st.error(f"👻 Oops! The correct answer was: {current_q['correct_answer']}")
                    
                    # Move to next question
                    st.session_state.current_question += 1
                    st.session_state.time_remaining = 30

                    # Check if game is over
                    if st.session_state.current_question >= len(st.session_state.questions):
                        st.session_state.game_over = True
                        save_high_score()
                        # Play congrats and stop background if available
                        try:
                            st.session_state.quiz.play_sound('congrats')
                        except Exception:
                            pass
                        try:
                            st.session_state.quiz.stop_background()
                        except Exception:
                            pass

                    time.sleep(2)  # Show result briefly
                    st.rerun()
        
        # Handle time up
        if time_up:
            st.warning("⏰ Time's up!")
            st.session_state.current_question += 1
            st.session_state.time_remaining = 30

            if st.session_state.current_question >= len(st.session_state.questions):
                st.session_state.game_over = True
                save_high_score()
                # Play congrats and stop background if available
                try:
                    st.session_state.quiz.play_sound('congrats')
                except Exception:
                    pass
                try:
                    st.session_state.quiz.stop_background()
                except Exception:
                    pass

            time.sleep(2)
            st.rerun()

if __name__ == '__main__':
    main()