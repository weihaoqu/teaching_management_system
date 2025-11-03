# Project prompt summaries

This document lists the prompts you asked during this project and a one-sentence summary of my reply for each, for quick reflection.

1. "when i go to add a class, press the add class button, there is nothing add to my attendence manage system, con you help me fix it"
   - Summary: Diagnosed likely cause (frontend not sending JSON/form or missing fields) and provided a server POST handler that accepts JSON or form data, validates fields, and logs errors.

2. "with the fix you did above, can you incoporate the fix to my python code"
   - Summary: Applied the POST-handler fix to `app.py` so the server accepts JSON/form payloads and initializes class data correctly.

3. "the add class button is not working, and no class is added, it does not take me off the \"add class\" page."
   - Summary: Suggested debugging steps (DevTools Network) and a robust handler to return clear errors so the frontend can respond appropriately.

4. "https://github.com/weihaoqu/teaching_management_system.git can you push this application to the repo."
   - Summary: Explained why the initial push failed (no git identity) and provided exact git commands to configure identity and push.

5. "can you do the push change for me"
   - Summary: Ran git commands, configured identity, committed files, and pushed the repository to GitHub.

6. "can you generate a requirement.txt for this projec"
   - Summary: Added a `requirements.txt` with Flask and Flask-Cors (and optional gunicorn commented).

7. "can you now push this change to github"
   - Summary: Committed and pushed `requirements.txt` to the remote repo.

8. "The code works on local computer. BUT when i push to github and use on vercel hosting, it does not register when I click the buttons to add class and i get errors like '/api/classes ... 500' Understand this error"
   - Summary: Explained 500 errors indicate server-side failures on Vercel, noted Flask isn't a persistent server on Vercel and recommended checking Vercel function logs and options (external backend, serverless conversion, or DB).

9. "these are from vercel log" (POST 500s)
   - Summary: Updated `save_data()` to try writing to `/tmp` as a fallback and return errors instead of crashing, and asked to redeploy and inspect logs.

10. "(apply and push fixes) can you do the push change for me"
    - Summary: Committed the backend changes and pushed them to GitHub.

11. "DevTools index:508 Uncaught TypeError: Cannot read properties of null (reading 'classList') at showTab ..."
    - Summary: Replaced fragile `showTab` that used the global `event` with a robust implementation that accepts a tab name or element.

12. "so i dont get errors in dev tools console log but we do get this in vercel ... Uncaught TypeError ..."
    - Summary: Changed `selectClass` to call `showTab('students')` (named switch) to avoid passing invalid event-like objects and pushed the fix.

13. "push to github please" (several times)
    - Summary: Committed and pushed the requested changes (frontend/backend/data) each time.

14. "can you make the functionality of the add student modal include taking the student id I enter at the top and attachting that with @monmouth.edu to form the student email without e having to type it in. Also students show in the students and attendance sections prior to me even selecting a certain class. make it so I have to select a class before it shows any students, then it shows the students in the chosen class."
    - Summary: Updated the frontend to auto-generate email from student ID when blank and to require selecting a class before showing students/attendance, disabling related buttons until a class is chosen.

15. "WARNING:app:Could not write to attendance_data.json: [Errno 30] Read-only file system ... It works on local machine but on vercel it does not. it doesnt even show the students in the class despite being the json"
    - Summary: Made `load_data()` prefer the `/tmp` fallback (where serverless writes go) and improved logging; explained ephemeral /tmp and recommended a proper DB for persistent storage.

16. "Whats a simple way we can manage the class data where it saves correctly and doesnt disappear after 5 minutes."
    - Summary: Recommended either using a managed DB (Supabase/Firebase/Postgres) for persistence or hosting the Flask backend on a persistent service (Render/Railway) and described pros/cons.

17. "This app is hosted on vercel"
    - Summary: Explained Vercel serverless limitations and provided Supabase integration and persistent-host options with high-level steps.

18. "can you generate a file of all the prompts I have asked for this project, and also your answer(in a short summary). I want to use it for reflection."
    - Summary: Created this `docs/prompt_summaries.md` file listing prompts and one-line summaries.

---

If you want this file committed and pushed to GitHub, tell me and I will commit and push it for you.
