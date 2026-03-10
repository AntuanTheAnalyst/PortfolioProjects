document.addEventListener("DOMContentLoaded", function() {

    const writingArea = document.getElementById("writingArea")
    const wordCount = document.getElementById("wordCount")
    const timerDisplay = document.getElementById("timer")
    const closeBtn = document.querySelector(".btn-danger")
    const retryBtn = document.getElementById("retryBtn")

    let timer
    let countdownInterval  // declare countdown variable

    // X button
    closeBtn.addEventListener("click", function() {
        writingArea.value = ""
        wordCount.innerText = 0
        timerDisplay.innerText = 5

        clearTimeout(timer)
        clearInterval(countdownInterval)
    })

    // Retry button
    retryBtn.addEventListener("click", function() {
        const failScreen = document.getElementById("failScreen")
        failScreen.style.display = "none"

        timerDisplay.innerText = 5
        writingArea.value = ""
        wordCount.innerText = 0
        writingArea.focus()
    })

    // Delete text and show fail screen
    function deleteText() {
        clearInterval(countdownInterval)   // stop countdown

        writingArea.value = ""
        wordCount.innerText = 0

        const failScreen = document.getElementById("failScreen")
        failScreen.style.display = "flex"
    }

    // Typing event
    writingArea.addEventListener("input", function() {

        // Stop previous timers
        clearTimeout(timer)
        clearInterval(countdownInterval)

        // Reset timer
        let timeLeft = 5
        timerDisplay.innerText = timeLeft

        // Countdown every second
        countdownInterval = setInterval(function() {
            timeLeft--
            timerDisplay.innerText = timeLeft

            if (timeLeft <= 0) {
                clearInterval(countdownInterval)
            }
        }, 1000)

        // Delete text after 5s
        timer = setTimeout(function() {
            deleteText()
        }, 5000)

        // Word count (ignore 1-letter words)
        let text = writingArea.value
        let words = text.trim().split(/\s+/).filter(word => word.length > 1)
        wordCount.innerText = words.length
    })
})