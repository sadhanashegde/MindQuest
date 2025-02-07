import * as THREE from "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.min.js";

// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x222244); // Dark blue background

// Camera setup
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 5); // Ensure the camera is in front of the sphere

// Renderer setup
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Create sphere
const geometry = new THREE.SphereGeometry(1, 32, 32);
const material = new THREE.MeshStandardMaterial({ color: 0xA88BEB, roughness: 0.7, metalness: 0.2 });
const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

// Lighting setup
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5); // Soft overall light
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1.5); // Stronger light
directionalLight.position.set(5, 5, 5);
scene.add(directionalLight);

// Breathing animation variables
let scale = 1;
let growing = true;

function animate() {
    requestAnimationFrame(animate);

    if (growing) {
        scale += 0.0049;
        if (scale >= 2) growing = false;
    } else {
        scale -= 0.0049;
        if (scale <= 1) growing = true;
    }

    sphere.scale.set(scale, scale, scale);
    renderer.render(scene, camera);
}

// Adjust canvas on window resize
window.addEventListener("resize", () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});

// Start animation
animate();
