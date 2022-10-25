# Introduction:  
### *In Project Pacman 1, Pacman agent will search paths from maze to arrive at a certain destination and collect food efficiently. General search algorithms are implemented in order to fulfill different kinds of Pacman scenarios.*

------
**Main files to look at under Pacman 1 Folder**:   
  1. **search.py**: contains all the search algorithms.   
  2. **searchAgents.py**: contains all the search-based agents.   

------
**How to compile and run code**:   
  1. Download entire Pacman 1 folder   
  2. Open terminal and set the path to where the source code is located at   
  3. Command for Seeking one certain Food Dot using DFS(Depth First Search) based on 3 mazes:   
        > 3.1 python pacman.py -l tinyMaze -p SearchAgent  
          3.2 python pacman.py -l mediumMaze -p SearchAgent  
          3.3 python pacman.py -l bigMaze -z .5 -p SearchAgent  
  4. Command for Seeking one certain Food Dot using BFS(Breadth First Search):  
        > 4.1 python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs  
          4.2 python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5  
  5. Command for Seeking one certain Food Dot using UCS(Uniform Cost Search):  
        > 5.1 python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs  
          5.2 python pacman.py -l mediumDottedMaze -p StayEastSearchAgent  
          5.3 python pacman.py -l mediumScaryMaze -p StayWestSearchAgent  
  6. Command for Seeking one certain Food Dot using A* Search:  
        > 6.1 python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic  
  7. Command for Seeking one all corners in the maze:  
        > 7.1 python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem  
          7.2 python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem  
  8. Command for Seeking one all corners in the maze based on consistent heuristic function:  
        > 8.1 python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5  
  9. Command for eating all food dots in as few steps as possible:  
        > 9.1 python pacman.py -l testSearch -p AStarFoodSearchAgent  
  10. Command for Suboptimal Search:  
        > 10.1 python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5   





  

