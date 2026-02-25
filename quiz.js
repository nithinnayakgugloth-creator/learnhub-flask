function checkAnswers() {
    let score = 0;

    // Question 1
    if (document.querySelector('input[name="q1"]:checked')?.value === "correct") {
        score++;
    }

    // Question 2
    if (document.querySelector('input[name="q2"]:checked')?.value === "correct") {
        score++;
    }

    // Question 3
    if (document.querySelector('input[name="q3"]:checked')?.value === "correct") {
        score++;
    }

    document.getElementById("result").innerHTML =
        "Your Score: " + score + " / 3";
}