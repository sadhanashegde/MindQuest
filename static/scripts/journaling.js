const canvas = document.getElementById("journalCanvas");
const ctx = canvas.getContext("2d");

canvas.width = 600;
canvas.height = 400;
canvas.style.border = "2px solid black";
canvas.style.background = "white";

let painting = false;

// Get correct mouse position relative to canvas
function getMousePos(e) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    };
}

// Start Drawing
function startPosition(e) {
    painting = true;
    const pos = getMousePos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

// Stop Drawing
function stopPosition() {
    painting = false;
    ctx.beginPath(); // Reset path to prevent weird lines
}

// Draw on Canvas
function draw(e) {
    if (!painting) return;
    const pos = getMousePos(e);
    ctx.lineWidth = 3; // Adjust pen thickness
    ctx.lineCap = "round";
    ctx.strokeStyle = "black";
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
    ctx.moveTo(pos.x, pos.y);
}

// Event Listeners
canvas.addEventListener("mousedown", startPosition);
canvas.addEventListener("mouseup", stopPosition);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mouseout", stopPosition);

// Clear Canvas Button
document.getElementById("clearCanvas").addEventListener("click", function () {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});
