const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.width = 500;
canvas.height = 400;

let ball, paddle, bricks, isGameRunning, destroyedBricks;
const totalBricks = 4 * 5; // (4 rows * 5 columns)

function resetGame() {
    ball = { x: canvas.width / 2, y: canvas.height - 30, dx: 2, dy: -2, radius: 7 };
    paddle = { width: 70, height: 10, x: (canvas.width - 70) / 2 };
    bricks = [];
    isGameRunning = false;
    destroyedBricks = 0; // Reset broken brick count

    for (let row = 0; row < 4; row++) {
        for (let col = 0; col < 5; col++) {
            bricks.push({ x: col * 80 + 30, y: row * 30 + 30, width: 70, height: 20, broken: false });
        }
    }
}

function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = "#FF5733";
    ctx.fill();
    ctx.closePath();
}

function drawPaddle() {
    ctx.fillStyle = "#0095DD";
    ctx.fillRect(paddle.x, canvas.height - paddle.height, paddle.width, paddle.height);
}

function drawBricks() {
    bricks.forEach(brick => {
        if (!brick.broken) {
            ctx.fillStyle = "#34A853";
            ctx.fillRect(brick.x, brick.y, brick.width, brick.height);
        }
    });
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBall();
    drawPaddle();
    drawBricks();
}

function update() {
    if (!isGameRunning) return;

    ball.x += ball.dx;
    ball.y += ball.dy;

    // Ball-wall collision
    if (ball.x - ball.radius < 0 || ball.x + ball.radius > canvas.width) ball.dx *= -1;
    if (ball.y - ball.radius < 0) ball.dy *= -1;

    // Paddle collision
    if (
        ball.y + ball.radius > canvas.height - paddle.height &&
        ball.x > paddle.x &&
        ball.x < paddle.x + paddle.width
    ) {
        ball.dy *= -1;
    }

    // Ball falls down (Game Over)
    if (ball.y + ball.radius > canvas.height) {
        alert("Game Over! Try again.");
        resetGame();
        return;
    }

    // Brick collision
    bricks.forEach(brick => {
        if (!brick.broken && ball.x > brick.x && ball.x < brick.x + brick.width && ball.y > brick.y && ball.y < brick.y + brick.height) {
            ball.dy *= -1;
            brick.broken = true;
            destroyedBricks++;

            // WIN CONDITION: If all bricks are destroyed
            if (destroyedBricks === totalBricks) {
                alert("🎉 YOU WIN! 🎉");
                resetGame();
                return;
            }
        }
    });

    draw();
    requestAnimationFrame(update);
}

// Start Game Button Fix
document.getElementById("startGame").addEventListener("click", function () {
    if (!isGameRunning) {
        isGameRunning = true;
        update();
    }
});

// Reset Game Button Fix
document.getElementById("resetGame").addEventListener("click", function () {
    resetGame();
    draw(); // Redraw after resetting
});

// Paddle Movement
canvas.addEventListener("mousemove", (e) => {
    paddle.x = e.clientX - canvas.getBoundingClientRect().left - paddle.width / 2;
});

// Initialize Game
resetGame();
draw();
