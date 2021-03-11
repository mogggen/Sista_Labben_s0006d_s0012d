# Sista_Labben_s0006d_s0012d

# About
Två grupper ska i Nebula Game Engine slå ihop kod från tidigare labbar för att slås med soldater och samla resurser.

# Setup
* instruktioner för att aktivera Nebula Engine: https://ltu.instructure.com/courses/12326/assignments/93299
* instruktioner för att utföra Labb 3.0: https://ltu.instructure.com/courses/12326/assignments/95826 i spelmotorarkitektur, S0012D
* pulla detta repository via: https://github.com/sirAgg/Sista_Labben_s0006d_s0012d.git

posta idéer och frågor via: https://github.com/sirAgg/Sista_Labben_s0006d_s0012d/issues

# Main objectives
The main goal of this assignment is to create an AI based on the former assignments that is able to produce soldiers and can attack another player and to use Nebula and the modifications you made earlier to achieve the task.

# Project setup
The assignment will be done in two teams with the AIs competing/fighting against each other.

The teams will have to decide on how to communicate things like damage, position, etc between each other.

Teams are picked by yourself, join one of the two teams in the "Group Project" groups in this canvas room. Create one git project in total that contains the main application and each groups AI components. You should split the groups code into separate folders to avoid conflicts. Avoid looking at each others code as well.

# Requirements
Each team has their own castle that they should defend. If the castle is destroyed, the other team wins.
There should be the same units, buildings and objects as in the previous AI assignment.
Add health to all units and buildings.
You are required to have a HUD using that shows the state of the simulation (resources collected etc.)
Implement this using ImGui (dynui in Nebula)
All properties like health, damage of weapons, probability of hitting, resources, speed, construction times are to be configurable via a script or some text file
Some sort of fog of war effect should be implemented
The battleground is: "mdl:environment/Groundplane.n3"
Use the navigation mesh provided in the files directory on canvas
Here are all the assets, including a small code snippet that sets up the battleground:

nota.cc https://github.com/sirAgg/Sista_Labben_s0006d_s0012d/blob/4491a66d555b25f18e3678b423909ad23b4ed922/nota.cc

assets.zip https://github.com/sirAgg/Sista_Labben_s0006d_s0012d/blob/4491a66d555b25f18e3678b423909ad23b4ed922/assets.zip

export_navigation.zip https://github.com/sirAgg/Sista_Labben_s0006d_s0012d/blob/4491a66d555b25f18e3678b423909ad23b4ed922/export_navigation.zip

The export_navigation archive can be unzipped directly to the export folder. This contains a simplified nav-mesh. There are no duplicate vertices or edges.
Checkout Legacy::Nvx2StreamReader - for loading meshes on CPU
        You can find an example in streamcolliderpool.cc:23 - Make sure to set the "Raw" flag so that it does not upload the mesh to the GPU.

# Optional
Units have animations that are controlled by the AI system
Sound effects
Examination:
The two teams AIs will battle each other (locally on the same machine/process, no networking required). Present this over zoom. Upload the Github repository link.

Each team will write a post mortem hand them in as a submission to this assignment. Provide a link to the github repositories for each of the teams, and also for the collaborated "core" code.

Each individual developer will also write a post mortem separately: See the "Post-mortem" assignment.