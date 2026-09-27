import requests
import streamlit as st
import hashlib
from io import BytesIO
from groq import Groq


from audio_recorder_streamlit import audio_recorder
from interview_evaluator import evaluate_interview



import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

browser_video_recorder = st.components.v2.component(
    "browser_video_recorder",

    html="""
        <div>
            <video
                id="preview"
                autoplay
                muted
                playsinline
                style="width:100%; max-width:640px; border-radius:12px;"
            ></video>

            <div style="margin-top:12px;">
                <button id="start">▶ Start Recording</button>
                <button id="stop" disabled>⏹ Stop Recording</button>
            </div>

            <p id="status">Ready</p>
        </div>
    """,

    css="""
        button {
            padding: 10px 16px;
            margin-right: 8px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
        }

        #start {
            background: #ff4b4b;
            color: white;
        }

        #stop {
            background: #444;
            color: white;
        }

        #status {
            margin-top: 10px;
            font-weight: 600;
        }
    """,

    js="""
        export default function(component) {

            const {
                parentElement,
                data,
                setStateValue
            } = component;

            const video = parentElement.querySelector("#preview");
            const startButton = parentElement.querySelector("#start");
            const stopButton = parentElement.querySelector("#stop");
            const status = parentElement.querySelector("#status");

            let stream = null;
            let recorder = null;
            let chunks = [];

            startButton.onclick = async () => {

                try {

                    status.textContent =
                        "Requesting camera and microphone...";

                    stream =
                        await navigator.mediaDevices.getUserMedia({
                            video: true,
                            audio: true
                        });

                    video.srcObject = stream;

                    const mimeTypes = [
                        "video/webm;codecs=vp9,opus",
                        "video/webm;codecs=vp8,opus",
                        "video/webm"
                    ];

                    const mimeType = mimeTypes.find(
                        type => MediaRecorder.isTypeSupported(type)
                    );

                    recorder = mimeType
                        ? new MediaRecorder(
                            stream,
                            { mimeType }
                        )
                        : new MediaRecorder(stream);

                    chunks = [];

                    recorder.ondataavailable = (event) => {

                        if (event.data.size > 0) {
                            chunks.push(event.data);
                        }

                    };

                    recorder.onstop = async () => {

                        status.textContent =
                            "Uploading video...";

                        const blob = new Blob(
                            chunks,
                            {
                                type:
                                    recorder.mimeType ||
                                    "video/webm"
                            }
                        );

                        const formData = new FormData();

                        formData.append(
                            "video",
                            blob,
                            "interview_video.webm"
                        );

                        const url =
                            `${data.apiBaseUrl}` +
                            `/interviews/` +
                            `${data.interviewId}` +
                            `/video` +
                            `?question_number=` +
                            `${data.questionNumber}`;

                        try {

                            const response =
                                await fetch(
                                    url,
                                    {
                                        method: "POST",
                                        body: formData
                                    }
                                );

                            if (response.ok) {

                                status.textContent =
                                    "✅ Video uploaded successfully!";

                                setStateValue(
                                    "status",
                                    "uploaded"
                                );

                            } else {

                                const errorText =
                                    await response.text();

                                status.textContent =
                                    "❌ Upload failed";

                                setStateValue(
                                    "status",
                                    "error"
                                );

                                setStateValue(
                                    "error",
                                    errorText
                                );
                            }

                        } catch (error) {

                            status.textContent =
                                "❌ Upload failed";

                            setStateValue(
                                "status",
                                "error"
                            );

                            setStateValue(
                                "error",
                                error.message
                            );
                        }

                        stream
                            .getTracks()
                            .forEach(
                                track => track.stop()
                            );

                        video.srcObject = null;

                    };

                    recorder.start();

                    startButton.disabled = true;
                    stopButton.disabled = false;

                    status.textContent =
                        "🔴 Recording...";

                } catch (error) {

                    status.textContent =
                        "❌ Camera/microphone error: " +
                        error.message;
                }
            };

            stopButton.onclick = () => {

                if (
                    recorder &&
                    recorder.state !== "inactive"
                ) {
                    recorder.stop();
                }

                startButton.disabled = false;
                stopButton.disabled = true;
            };
        }
    """
)



    

# ---------------- Interview ID ----------------

interview_id = st.query_params.get("interview_id")


# ---------------- Load Interview ----------------

if not interview_id:

    st.error("❌ Invalid interview link.")

    st.stop()


response = requests.get(
   f"{API_BASE_URL}/interviews/{interview_id}"
)

if response.status_code != 200:

    st.error("❌ Interview not found.")

    st.stop()


interview = response.json()


# ---------------- Interview Data ----------------

candidate_name = interview["candidate"]
interview_date = interview["date"]
interview_mode = interview["mode"]
questions = interview["questions"]


# ---------------- Page Configuration ----------------

st.set_page_config(
    page_title="TalentMatch AI - Interview Portal",
    page_icon="🎤",
    layout="centered"
)


st.title("🤖 TalentMatch AI")
st.subheader("🎤 Interview Portal")

st.divider()

st.header(f"Welcome, {candidate_name}! 👋")

st.write(
    "You have been invited to complete an interview through TalentMatch AI."
)

st.info(
    "Please read the instructions carefully before starting your interview."
)

st.markdown("### 📋 Interview Instructions")

st.write("✅ Make sure you have a stable internet connection.")
st.write("✅ Find a quiet environment.")
st.write("✅ Make sure your microphone is working.")
st.write("✅ Read each question carefully.")
st.write("✅ Take your time and answer clearly.")

st.divider()

st.markdown("### 📅 Interview Details")

st.write(f"**Candidate:** {candidate_name}")
st.write(f"**Date:** {interview_date}")
st.write(f"**Mode:** {interview_mode}")

st.divider()


# ---------------- Start Interview ----------------

if "interview_started" not in st.session_state:

    st.session_state.interview_started = False
    
if "interview_completed" not in st.session_state:
    st.session_state.interview_completed = False


if st.button("🎤 Start Interview"):

    st.session_state.interview_started = True


if st.session_state.interview_started:

    st.success("✅ Interview started!")

    # --------------------------
    # Current Question
    # --------------------------

    if "current_question" not in st.session_state:
        st.session_state.current_question = 0

    if "answers" not in st.session_state:
        st.session_state.answers = {}
        
    if "transcripts" not in st.session_state:
        st.session_state.transcripts = {}
        
    if "last_audio_hash" not in st.session_state:
        st.session_state.last_audio_hash = None

    current_question = st.session_state.current_question
    st.markdown(
        f"### 🎤 Question {current_question + 1} of {len(questions)}"
    )

    st.write(questions[current_question])
    st.markdown("### 🎥 Video Interview")

    st.info(
        "🎥 Click START to begin recording your answer. "
        "Click STOP when you have finished answering."
    )

    video_result = browser_video_recorder(
        data={
            "apiBaseUrl": API_BASE_URL,
            "interviewId": interview_id,
            "questionNumber": current_question + 1
        },
        key=f"browser_video_{current_question}"
    )
                
    st.write("🎙️ Or answer by speaking:")

    audio = audio_recorder(
    text="🎙️ Record Answer",
    recording_color="#ff4b4b",
    neutral_color="#6c757d",
    icon_name="microphone",
    icon_size="2x"
    )

    if audio:
        audio_hash = hashlib.md5(audio).hexdigest()

        if audio_hash != st.session_state.last_audio_hash:

            st.session_state.last_audio_hash = audio_hash

            with st.spinner("🤖 Transcribing your answer..."):

                audio_file = BytesIO(audio)
                audio_file.name = "answer.wav"

                transcription = groq_client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3-turbo",
                    response_format="json",
                    language="en",
                    temperature=0.0
                )

            transcript = transcription.text

            st.session_state.transcripts[current_question] = transcript
            st.session_state[f"answer_{current_question}"] = transcript

            st.success("✅ Transcription complete!")


    # --------------------------
    # Candidate Answer
    # --------------------------

    answer = st.text_area(
        "📝 Your Answer",
        key=f"answer_{current_question}",
        height=150
    )

    # --------------------------
    # Next Question
    # --------------------------

    if current_question < len(questions) - 1:


            if st.button("Next →"):

                st.session_state.answers[current_question] = answer

                st.session_state.current_question += 1

                next_question = st.session_state.current_question

                st.session_state[f"answer_{next_question}"] = ""
                st.session_state.transcripts[next_question] = ""

                st.rerun()

                st.session_state.current_question += 1

                next_question = st.session_state.current_question

                st.session_state[f"answer_{next_question}"] = ""
                st.session_state.transcripts[next_question] = ""

                st.rerun()

    else:

        if not st.session_state.interview_completed:

            if st.button("🏁 Submit Interview"):

                st.session_state.answers[current_question] = answer


                if mp4_file:
                    st.success("✅ Final video saved successfully!")

                st.session_state.interview_completed = True

                with st.spinner("🤖 Evaluating your interview..."):

                    evaluation = evaluate_interview(
                        questions,
                        st.session_state.answers
                    )

                    evaluation_response = requests.put(
                        f"{API_BASE_URL}/interviews/{interview_id}/evaluation",
                        json=evaluation.model_dump()
                    )

                if evaluation_response.status_code == 200:
                    st.success("🎉 Interview submitted successfully!")
                else:
                    st.error("❌ Failed to save interview evaluation.")
                    st.write(evaluation_response.text)

                st.markdown("## 📊 Interview Evaluation")

                st.metric(
                    "Overall Score",
                    f"{evaluation.overall_score} / 100"
                )

                st.divider()

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Technical Knowledge",
                        f"{evaluation.technical_knowledge} / 100"
                    )

                with col2:
                    st.metric(
                        "Communication",
                        f"{evaluation.communication} / 100"
                    )

                with col3:
                    st.metric(
                        "Problem Solving",
                        f"{evaluation.problem_solving} / 100"
                    )

                st.divider()

                st.markdown("### 💪 Strengths")

                for strength in evaluation.strengths:
                    st.write(f"• {strength}")

                st.markdown("### 📈 Areas for Improvement")

                for area in evaluation.areas_for_improvement:
                    st.write(f"• {area}")

                st.markdown("### 🎯 Recommendation")

                st.info(evaluation.recommendation)

                st.markdown("### 💬 Brief Feedback")

                st.write(evaluation.brief_feedback)