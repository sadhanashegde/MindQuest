# MindQuest

git init
git add .
git status (after you do this, everything should be in green like the file name n all)
git commit -m "put some message here; indicating what u did like the feature u just added"
git branch -M main
git push -u origin main


**Steps for collaborators:**

[Clone the project in your pc:]
git clone https://github.com/name/MindQuest.git

[Go to the directory:]
cd MindQuest

[Create a new branch because working on others branch maybe harmful:]
git checkout -b feature-branch

[Pull: (idk what)]
git pull origin main

[After adding a feature make sure you push it to the GitHub.]
[Adds all the file to staging area]
git add . 

[Commits the changes]
git commit -m "Added feature X"

[Push your feature to the origin branch]
git push origin feature-branch

They should go to GitHub and create a Pull Request (PR) to merge their branch into main.
git checkout main
git pull origin main
git pull origin main
