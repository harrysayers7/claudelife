# Voice Input Configuration

Process voice inputs through speech-to-text pipeline:

1. **Voice Note Processing**
   - Accept audio file paths
   - Transcribe using Whisper/OpenAI API
   - Process natural language commands
   - Execute appropriate actions

2. **Voice Command Patterns**
   - "Hey Claude..." → Wake word activation
   - "Quick note..." → Instant capture
   - "Start recording..." → Meeting transcription
   - "Voice memo..." → Personal notes

3. **Output Format**
   Save transcriptions to memory/voice/[date]/
   - Raw transcript
   - Processed commands
   - Executed actions
   - Audio file reference