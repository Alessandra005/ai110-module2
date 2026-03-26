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
    Task priority (high/medium/low) and the
    owner's available time budget (available_minutes). Priority is the primary constraint because missing a high priority task like feeding or medication has a great impact on the pet. Time is the next constraint so the scheduler stops adding tasks
    once the budget is full.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
    The conflict detection only flags tasks with the exact same scheduled_time string. It does not really check whether task durations overlap. It is reasonable though, because this keeps the code easy to understand, and since exact time mistakes are most common, it still catches the main problem without making things complicated.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
    I used GitHub Copilot Chat throughout the project. Mostly for design brainstorming like creating the first UML and class outlines, for code review where it helped me find missing links and slow parts in pawpal_system.py, and for test generation where it helped draft pytest tests for edge cases I might have missed. The most helpful way to use it was giving the file with #file so Copilot had the full context before answering.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
    At the beginning, Copilot suggested adding a pet field inside each Task so the scheduler could show which pet it belonged to. I chose not to do that because it would create a loop where Pets contain Tasks and Tasks point back to Pets, which would make the design messy. So, instead, I handled the display in the UI by looking up the pet name from the owner’s list when showing the schedule. This kept the design simple and avoided unnecessary coupling.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
    I tested the whole task flow to make sure completed tasks never get rescheduled, daily and weekly repeats create new tasks correctly, and priorities and time limits are handled the right way. I also checked that conflicts are detected only when they should be. These were important because they confirmed that the scheduler behaves predictably and doesn’t create unexpected tasks or ordering mistakes.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
    I’m confident in the scheduler because the most important edge cases are already covered. If I had more time, I would test a task whose duration exactly matches the remaining time budget and also check how recurrence behaves across a month boundary. Right now, I’d put my confidence at about a 4/5.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I’m most happy with how clean the class structure turned out. Keeping Pet as the data holder, Owner as the aggregator, and Scheduler as the consumer made everything easier to reason about and test. Using dataclasses also helped keep Task and Pet simple without a lot of extra code.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I would build a proper real time of day scheduling engine so the plan shows an actual timeline instead of just a sorted list. I’d also upgrade conflict detection so it checks for overlapping durations, not just identical start times.


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    Designing the UML before writing any code forced me to think through class responsibilities upfront, which really made the final design cleaner, and when working with AI, it is definetely crucial to know when to accept a suggestion and when to push back so the design stays consistent.
