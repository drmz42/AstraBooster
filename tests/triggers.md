# Trigger cases

Use these to check the description when implicit invocation is enabled. Record the host, its version and whether invocation was manual or automatic.

## Should activate

1. "Fix the signup form: users see the success page but no account is created."
2. "Add a webhook handler that stores payment status updates."
3. "The nightly export job stopped writing files; find out why and fix it."
4. "Make the dashboard's Export button work and check it on mobile."
5. "Connect the support bot to the ticket API and confirm tickets are created."
6. "Take over this half-finished queue migration from another agent."
7. "Refactor the order service across four modules without changing behavior."

## Should not activate

1. "What does this regular expression match?"
2. "Fix the typo in the README heading."
3. "Change the button color to the brand blue."
4. "Rename this local variable for clarity."
5. "Add a unit test for this pure date-formatting function."
6. "Summarize the last five commits."

## Accept

All "should activate" cases load the skill and none of the "should not activate" cases do. A miss is a description defect, not a model defect; record it with the exact wording.
