const pieces = document.querySelectorAll(".puzzle-piece");

pieces.forEach(piece => {
    piece.addEventListener("dragstart", dragStart);
    piece.addEventListener("dragover", dragOver);
    piece.addEventListener("drop", drop);
});

function dragStart(event) {
    event.dataTransfer.setData("text", event.target.id);
}

function dragOver(event) {
    event.preventDefault();
}

function drop(event) {
    event.preventDefault();
    const pieceId = event.dataTransfer.getData("text");
    const draggedPiece = document.getElementById(pieceId);
    event.target.appendChild(draggedPiece);
}
