import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.module.js";

// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

const canvasSize = 600; // 🔥 Black canvas size
renderer.setSize(canvasSize, canvasSize);
renderer.domElement.style.display = "block";
renderer.domElement.style.margin = "auto";
document.body.appendChild(renderer.domElement);
renderer.setSize(600, 600); // 🔥 Canvas size


// Game variables
let gameActive = true;
const snake = [];
const segmentSize = 2; // 🔥 Thinner Snake
let direction = new THREE.Vector3(1, 0, 0);
let moveDelay = 250; // 🔥 Balanced speed
let lastMoveTime = 0;
const moveQueue = [];
const gameAreaWidth = 80; // 🔥 Wider Play Area
const gameAreaHeight = 35; // 🔥 Shorter Height
const playAreaSize = gameAreaWidth; // 🔥 Make sure playArea == gameArea
let selfCollisionCount = 0;

// Create snake head (Yellow)
const head = new THREE.Mesh(
    new THREE.BoxGeometry(segmentSize, segmentSize, segmentSize),
    new THREE.MeshBasicMaterial({ color: 0xffff00 }) // Yellow head
);
head.position.set(0, 0, 0);
snake.push(head);
scene.add(head);

// Create snake body (Green)
for (let i = 1; i < 3; i++) {
    const segment = new THREE.Mesh(
        new THREE.BoxGeometry(segmentSize, segmentSize, segmentSize),
        new THREE.MeshBasicMaterial({ color: 0x44ff44 }) // Green body
    );
    segment.position.set(-i * segmentSize, 0, 0);
    snake.push(segment);
    scene.add(segment);
}

// Create food (Red, Square Shape)
const food = new THREE.Mesh(
    new THREE.BoxGeometry(segmentSize * 0.8, segmentSize * 0.8, segmentSize * 0.8),
    new THREE.MeshBasicMaterial({ color: 0xff4444 }) // Red food
);
scene.add(food);
placeFood();

// 🔥 Create Border (White Box)
const borderMaterial = new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 2 }); // White border
const borderGeometry = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(-gameAreaWidth, -gameAreaHeight, 0),  // Bottom-left
    new THREE.Vector3(gameAreaWidth, -gameAreaHeight, 0),   // Bottom-right
    new THREE.Vector3(gameAreaWidth, gameAreaHeight, 0),    // Top-right
    new THREE.Vector3(-gameAreaWidth, gameAreaHeight, 0),   // Top-left
    new THREE.Vector3(-gameAreaWidth, -gameAreaHeight, 0)   // Back to Bottom-left
]);

const border = new THREE.Line(borderGeometry, borderMaterial);
scene.add(border);

// Position camera
camera.position.set(0, 0, 50);
camera.lookAt(0, 0, 0);

// Game loop
function animate(time) {
    if (!gameActive) return; // Stop if game over

    requestAnimationFrame(animate);

    if (time - lastMoveTime > moveDelay) {
        lastMoveTime = time;

        if (moveQueue.length) {
            direction = moveQueue.shift();
        }

        let newHeadPos = snake[0].position.clone().add(direction.clone().multiplyScalar(segmentSize));

        // 🔥 Check boundary collision (Game Over)
        if (
            newHeadPos.x >= gameAreaWidth || newHeadPos.x <= -gameAreaWidth ||
            newHeadPos.y >= gameAreaHeight || newHeadPos.y <= -gameAreaHeight
        ) {
            endGame();
            return;
        }


        // 🔥 Check self-collision
        for (let i = 1; i < snake.length; i++) {
            if (newHeadPos.distanceTo(snake[i].position) < 0.1) {
                selfCollisionCount++;
                if (selfCollisionCount >= 2) {
                    endGame();
                    return;
                } else {
                    shrinkSnake(i);
                }
                break;
            }
        }

        // Move the body
        for (let i = snake.length - 1; i > 0; i--) {
            snake[i].position.copy(snake[i - 1].position);
        }
        snake[0].position.copy(newHeadPos);

        // Food collision
        if (snake[0].position.distanceTo(food.position) < segmentSize * 0.5) {
            growSnake();
            placeFood();
        }
    }

    renderer.render(scene, camera);
}

// Place food randomly within the play area
function placeFood() {
    food.position.set(
        Math.floor((Math.random() * (gameAreaWidth * 2 - segmentSize)) - gameAreaWidth + segmentSize / 2),
        Math.floor((Math.random() * (gameAreaHeight * 2 - segmentSize)) - gameAreaHeight + segmentSize / 2),
        0
    );

}

// Grow snake
function growSnake() {
    const lastSegment = snake[snake.length - 1];
    const newSegment = new THREE.Mesh(
        new THREE.BoxGeometry(segmentSize, segmentSize, segmentSize),
        new THREE.MeshBasicMaterial({ color: 0x44ff44 }) // Green
    );
    newSegment.position.copy(lastSegment.position);
    snake.push(newSegment);
    scene.add(newSegment);
}

// Shrink snake on first self-collision
function shrinkSnake(index) {
    for (let i = snake.length - 1; i >= index; i--) {
        scene.remove(snake[i]);
        snake.pop();
    }
}

// End game logic
function endGame() {
    gameActive = false;
    alert("Game Over! 🐍💀");
}

// Keyboard Controls
window.addEventListener("keydown", (event) => {
    if (!gameActive) return; // No movement after game over

    const newDirection = {
        ArrowUp: new THREE.Vector3(0, 1, 0),
        ArrowDown: new THREE.Vector3(0, -1, 0),
        ArrowLeft: new THREE.Vector3(-1, 0, 0),
        ArrowRight: new THREE.Vector3(1, 0, 0)
    }[event.key];

    if (newDirection && !newDirection.equals(direction.clone().multiplyScalar(-1))) {
        moveQueue.push(newDirection);
    }
});

animate();
