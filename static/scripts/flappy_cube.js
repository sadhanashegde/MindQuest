
// Initialize scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.OrthographicCamera(
  window.innerWidth / -100,
  window.innerWidth / 100,
  window.innerHeight / 100,
  window.innerHeight / -100,
  1,
  1000
);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Create smaller player cube
const cubeGeometry = new THREE.BoxGeometry(0.5, 0.5, 0); // Smaller size
const cubeMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
scene.add(cube);

cube.position.y = 0;
camera.position.z = 5;

let velocityY = 0;
const gravity = -0.005;
const flapStrength = 0.1;

// Obstacles
const obstacles = [];
const obstacleSpeed = 0.02;
const obstacleGap = 2.5; // Larger gap for easier gameplay

function createObstacle(xPos) {
  const gapY = Math.random() * 4 - 2;

  // Top obstacle
  const topGeometry = new THREE.PlaneGeometry(1, 10);
  const topMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
  const topObstacle = new THREE.Mesh(topGeometry, topMaterial);
  topObstacle.position.set(xPos, gapY + obstacleGap / 2 + 5, 0);

  // Bottom obstacle
  const bottomGeometry = new THREE.PlaneGeometry(1, 10);
  const bottomMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
  const bottomObstacle = new THREE.Mesh(bottomGeometry, bottomMaterial);
  bottomObstacle.position.set(xPos, gapY - obstacleGap / 2 - 5, 0);

  scene.add(topObstacle, bottomObstacle);

  return { top: topObstacle, bottom: bottomObstacle };
}

// Spawn initial obstacles
for (let i = 0; i < 5; i++) {
  obstacles.push(createObstacle(i * 5 + 10));
}

let gameStarted = false;

function countdownTimer(callback) {
  let countdown = 5;
  const countdownText = document.createElement("div");
  countdownText.style.position = "absolute";
  countdownText.style.top = "50%";
  countdownText.style.left = "50%";
  countdownText.style.transform = "translate(-50%, -50%)";
  countdownText.style.color = "white";
  countdownText.style.fontSize = "48px";
  countdownText.style.zIndex = "2";
  document.body.appendChild(countdownText);

  const interval = setInterval(() => {
    countdownText.textContent = `Game starts in: ${countdown}`;
    countdown--;
    if (countdown < 0) {
      clearInterval(interval);
      countdownText.style.display = "none";
      callback();
    }
  }, 1000);
}

// Handle key presses
document.addEventListener("keydown", (event) => {
  if (event.code === "Space" && gameStarted) {
    velocityY = flapStrength;
  }
});

function updateObstacles() {
  obstacles.forEach((obstacle) => {
    obstacle.top.position.x -= obstacleSpeed;
    obstacle.bottom.position.x -= obstacleSpeed;

    // Reset obstacle position when off-screen
    if (obstacle.top.position.x < -5) {
      obstacle.top.position.x += 25;
      obstacle.bottom.position.x += 25;

      const gapY = Math.random() * 4 - 2;
      obstacle.top.position.y = gapY + obstacleGap / 2 + 5;
      obstacle.bottom.position.y = gapY - obstacleGap / 2 - 5;
    }
  });
}

function checkCollision() {
  for (const obstacle of obstacles) {
    const topBox = new THREE.Box3().setFromObject(obstacle.top);
    const bottomBox = new THREE.Box3().setFromObject(obstacle.bottom);
    const cubeBox = new THREE.Box3().setFromObject(cube);

    if (topBox.intersectsBox(cubeBox) || bottomBox.intersectsBox(cubeBox)) {
      alert("Game Over! Press OK to Restart.");
      window.location.reload();
    }
  }

  if (cube.position.y < -5 || cube.position.y > 5) {
    alert("Game Over! Press OK to Restart.");
    window.location.reload();
  }
}

function animate() {
  requestAnimationFrame(animate);

  if (gameStarted) {
    // Apply gravity and update cube position
    velocityY += gravity;
    cube.position.y += velocityY;

    // Update obstacles
    updateObstacles();

    // Check collisions
    checkCollision();
  }

  renderer.render(scene, camera);
}

countdownTimer(() => {
  gameStarted = true;
});

animate();
