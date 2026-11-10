Today (10 Nov), I initiated the project using FastAPI as our backend server, integrated OpenRouter via its API key, and wired up the OpenAI client SDK.

I also explored how **temperature** works: LLMs calculate statistical probabilities for every next token, and temperature scales those probabilities. Low temperatures make the model strict and predictable by choosing the most probable words, while high temperatures ($1.0+$) flatten the probability distribution, making less likely words more probable for creative outputs. When testing a high temperature on a simple prompt ("Say something 3 times"), the output turned into chaotic nonsense.

Additionally, I built real-time streaming using **Server-Sent Events (SSE)**, the standard for LLMs. Streaming prevents users from staring at a blank screen during heavy responses by pushing text chunks instantly as they arrive. The backend now exposes 3 endpoints: a health check, a standard AI call, and a streaming call.
