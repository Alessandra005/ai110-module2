# PawPal+ Project Reflection

## 1. System Design
    3 core actions:
    1. Add a pet and enter basic info
    2. Add care tasks to a pet with duration and priority
    3. Generate and view a prioritised daily schedule with an explanation.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
    There should be 4 classes:
    - Task: With title, duration, priority, completion status. 
    - Pet: Stores a pet's profile (name, species, age) and owns a list of Tasks. 
    - Owner: Represents the human user with a time budget and a list of Pets. Responsible for aggregating all tasks across pets so the Scheduler has a single entry point.
    - Scheduler: Receives an Owner, walks the combined task list, and builds a daily schedule that fits within the owner's available time.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    After Copilot reviewed the skeleton it flagged 5 issues. I decided to just apply 3 of them.

    Changes made:
    - Added a `completed` check inside `build_schedule()` so completed tasks are not rescheduled.
    - Changed `explain_plan()` so the code runs quicker.
    - Added a guard and warning to `filter_by_priority()`.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
    The conflict detection only flags tasks with the exact same scheduled_time string. It does not really check whether task durations overlap. It is reasonable though, because this keeps the code easy to understand, and since exact time mistakes are most common, it still catches the main problem without making things complicated.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
