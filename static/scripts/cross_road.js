// Initialize scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Lighting
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(10, 10, 10);
scene.add(light);

// Create the road path
const roadTexture = new THREE.TextureLoader().load("https://i.imgur.com/WZpAjS9.jpeg");
const roadMaterial = new THREE.MeshStandardMaterial({ map: roadTexture });
const roadGeometry = new THREE.PlaneGeometry(20, 50); // Road length 50 units
const road = new THREE.Mesh(roadGeometry, roadMaterial);
road.rotation.x = -Math.PI / 2;
scene.add(road);

// Create the player block (yellow cube)
const playerMaterial = new THREE.MeshStandardMaterial({ color: 0xffff00 });
const playerGeometry = new THREE.BoxGeometry(1.5, 1.5, 1.5);
const player = new THREE.Mesh(playerGeometry, playerMaterial);
player.position.set(0, 0.75, -24);
scene.add(player);

// Create the start line
const startGeometry = new THREE.PlaneGeometry(20, 1);
const startMaterial = new THREE.MeshStandardMaterial({ color: 0x32cd32 });
const startLine = new THREE.Mesh(startGeometry, startMaterial);
startLine.rotation.x = -Math.PI / 2;
startLine.position.set(0, 0.01, -24);
scene.add(startLine);

// Create the finish line
const finishGeometry = new THREE.PlaneGeometry(20, 1);
const finishMaterial = new THREE.MeshStandardMaterial({ color: 0xffd700 });
const finishLine = new THREE.Mesh(finishGeometry, finishMaterial);
finishLine.rotation.x = -Math.PI / 2;
finishLine.position.set(0, 0.01, 24);
scene.add(finishLine);

// Obstacles (smooth gliding)
const obstacles = [];
for (let i = 0; i < 10; i++) {
  const obstacleGeometry = new THREE.BoxGeometry(2, 1, 1);
  const obstacleMaterial = new THREE.MeshStandardMaterial({ color: 0xff0000 });
  const obstacle = new THREE.Mesh(obstacleGeometry, obstacleMaterial);

  const zPos = (i + 1) * 4 - 22; // Avoid start and finish line areas

  obstacle.position.set(
    (Math.random() - 0.5) * 18, // Random X position
    0.5,
    zPos
  );

  obstacle.userData.direction = Math.random() > 0.5 ? 0.05 : -0.05;
  obstacles.push(obstacle);
  scene.add(obstacle);
}

// Camera setup
camera.position.set(0, 15, 35);
camera.lookAt(0, 0, 0);

// Player controls
const playerSpeed = 0.5;
const keys = {};
document.addEventListener("keydown", (event) => {
  keys[event.code] = true;
});
document.addEventListener("keyup", (event) => {
  keys[event.code] = false;
});

// Handle Replay Button
document.getElementById("replay-btn").addEventListener("click", () => {
  resetGame();
  document.getElementById("game-over").style.display = "none";
});
document.getElementById("replay-btn-win").addEventListener("click", () => {
  resetGame();
  document.getElementById("win-message").style.display = "none";
});

// Reset Game Function
function resetGame() {
  player.position.set(0, 0.75, -24);
  obstacles.forEach((obstacle) => {
    obstacle.position.set(
      (Math.random() - 0.5) * 18,
      0.5,
      Math.random() * 40 - 20
    );
  });
}

// Animation loop
function animate() {
  requestAnimationFrame(animate);

  // Move the player
  if (keys["ArrowUp"]) player.position.z += playerSpeed;
  if (keys["ArrowDown"]) player.position.z -= playerSpeed;
  if (keys["ArrowLeft"]) player.position.x -= playerSpeed;
  if (keys["ArrowRight"]) player.position.x += playerSpeed;

  // Prevent player from moving out of bounds
  player.position.x = Math.max(-9, Math.min(9, player.position.x));

  // Move obstacles smoothly
  obstacles.forEach((obstacle) => {
    obstacle.position.x += obstacle.userData.direction;

    // Reverse direction at edges
    if (obstacle.position.x > 9 || obstacle.position.x < -9) {
      obstacle.userData.direction *= -1;
    }

    // Check collision
    if (
      Math.abs(player.position.x - obstacle.position.x) < 1.25 &&
      Math.abs(player.position.z - obstacle.position.z) < 1
    ) {
      document.getElementById("game-over").style.display = "block";
      return;
    }
  });

  // Check if player crosses the road
  if (player.position.z > 23) { // Finish zone check
    document.getElementById("win-message").style.display = "block";
    return;
  }

  renderer.render(scene, camera);
}

animate();
