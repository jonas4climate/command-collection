import java.util.Scanner;

public class Connect {

   private int CONNECT_TO_WIN;

   private int X;
   private int Y;

   private String PLAYER1;
   private String PLAYER2;

   private Player[][] map;
   private Player playerOfTurn;
   private boolean gameRunning = true;
   private Scanner scanner;

   public static void main(String[] args) {
      Connect game = null;
      try {
         if (args.length == 3) {
            int connectToWin = Integer.parseInt(args[0]);
            int X = Integer.parseInt(args[1]);
            int Y = Integer.parseInt(args[2]);

            if (connectToWin > 1 && connectToWin <= X && connectToWin <= Y && X > 1 && Y > 1)
               game = new Connect(connectToWin, X, Y);
         }
      } catch (Exception e) {
         System.out.println("There has been invalid input. The default game was chosen instead.");
      }

      // If not initialized with proper paramters
      if (game == null)
         game = new Connect(4, 7, 6);
      game.run();
   }

   public void run() {
      setup();

      while (gameRunning) {
         gameStep();
      }
      scanner.close();
   }

   private void gameStep() {
      swapPlayerOfTurn();
      System.out.println(String.format("\nIt is %s's turn. You place '%s' discs.", getPlayerName(playerOfTurn), getSymbol(playerOfTurn)));

      System.out.print("Enter collumn to drop your disc in: ");
      
      // Very safe input
      String input = scanner.next();
      while (!inputIsValidInt(input)) {
         System.out.println("Invalid input. Please try again.");
         System.out.print("Enter collumn to drop your disc in: ");
         input = scanner.next();
      }
      int x = Integer.parseInt(input);

      // Drop disc into collumn
      for (int y = 0; y < Y; y++) {
         if (map[x][y] == null) {
            map[x][y] = playerOfTurn;
            break;
         }
      }

      displayGameState();

      if (isWin(x)) {
         System.out.println(String.format("\n%s has won!", getPlayerName(playerOfTurn)));
         gameRunning = false;
      }

      if (isDraw()) {
         System.out.println("It was a draw!");
         gameRunning = false;
      }
   }

   private void displayGameState() {
      StringBuilder state = new StringBuilder();
      state.append("\n");
      // Add map as string
      for (int y = Y-1; y >= 0; y--) {
         state.append(y);
         for (int x = 0; x < X; x++) {
            state.append(" " + getSymbol(map[x][y]));
         }
         state.append("\n");
      }

      state.append(' ');
      // Add for collumns below
      for (int i = 0; i < X; i++) {
         state.append(" " + i);
      }
      state.append("\n");
      System.out.println(state.toString());
   }

   private boolean inputIsValidInt(String input) {
      try {
         int x = Integer.parseInt(input);
         if (isValidInput(x))
            return true;
         else
            return false;
      } catch (Exception e) {
         return false;
      }
   }

   private boolean isWin(int xLastMove) {
      // Get highest disc of collumn
      int yLastMove = 0;
      for (int y = Y-1; y >= 0; y--) {
         if (map[xLastMove][y] != null) {
            yLastMove = y;
            break;
         }
      }

      // Use position of last disc to check for win condition quickly

      // use x and y as direction matricies
      // check for wins vertically, horizontally and diagonally
      for (int x = -1; x <= 1; x++) {
         for (int y = -1; y <= 1; y++) {
            if (!(x == 0 && y == 0) && withinBoundaries(xLastMove, yLastMove, x, y)) {
               boolean allInRow = true;
               for (int i = 1; i < CONNECT_TO_WIN; i++) {
                  if (map[xLastMove + i*x][yLastMove + i*y] != playerOfTurn)
                     allInRow = false;
               }
               if (allInRow)
                  return true;
            }
         }
      }
      return false;
   }
   
   private boolean withinBoundaries(int xLastMove, int yLastMove, int x, int y) {
      int mx = xLastMove + (CONNECT_TO_WIN-1)*x;
      int my = yLastMove + (CONNECT_TO_WIN-1)*y;
      if (mx < X && mx >= 0 && my < Y && my >= 0)
         return true;
      else
         return false;
   }

   private boolean isDraw() {
      for (int x = 0; x < X; x++) {
         if (map[x][Y-1] == null)
            return false;
      }
      return true;
   }

   private boolean isValidInput(int x_input) {
      // If within bounds of WIDTH and free disc spot at HEIGHT-1
      if (x_input >= 0 && x_input < X && map[x_input][Y-1] == null)
         return true;
      else
         return false;
   }

   private void setup() {
      System.out.println("Welcome to a Game of Connect " + CONNECT_TO_WIN + "!\n");
      scanner = new Scanner(System.in);

      System.out.print("Enter name of Player 1: ");
      PLAYER1 = scanner.nextLine();
      System.out.println(String.format("%s's occupied spots will be marked using an 'X'", PLAYER1));

      System.out.print("Enter name of Player 2: ");
      PLAYER2 = scanner.nextLine();
      System.out.println(String.format("%s's occupied spots will be marked using an 'O'", PLAYER2));

      gameRunning = true;
      playerOfTurn = Player.P1;
      displayGameState();
   }

   private void swapPlayerOfTurn() {
      if (playerOfTurn == Player.P1)
         playerOfTurn = Player.P2;
      else
         playerOfTurn = Player.P1;
   }

   private String getPlayerName(Player player) {
      if (player == Player.P1)
         return PLAYER1;
      else if (player == Player.P2)
         return PLAYER2;
      else
         return null;
      
   }

   private String getSymbol(Player player) {
      if (player == Player.P1)
         return "X";
      else if (player == Player.P2)
         return "O";
      else
         return "_";
   }

   /**
    * Verbose definition of Player
    */
   enum Player {
      P1,
      P2
   }

   /**
    * 
    * @param connect_to_win Number of discs in a row needed to win
    * @param width Width of the game area
    * @param height Height of the game area
    */
   public Connect(int connectToWin, int x, int y) {
      X = x;
      Y = y;
      CONNECT_TO_WIN = connectToWin;
      map = new Player[X][Y];
   }
}