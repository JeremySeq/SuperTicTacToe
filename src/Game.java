import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;


/**
 *
 * Two different rules, which do I use?:
 * 1. If a player has to move in a square that has already been won, they can choose any square to move in.
 * 2. If a player has to move in a square that has already been won, they must still move in that square (although
 *    they cannot win that square it still influences the next move)
 *
 */
public class Game extends JPanel implements ActionListener, MouseListener {

    public final InputHandler inputHandler = new InputHandler();

    public static final int WIDTH = 900;
    public static final int HEIGHT = 900;

    // 0 = none, 1 = x, 2 = o, 3 = /\
    public int[][][][] board = new int[3][3][3][3];

    // keeps track of the smaller simple 3x3 board and who has won each square
    public int [][] semi_board = new int[3][3];

    public int[] next_move_square = new int[2];

    public int currentTeam = 1;

    public final int DELAY = 10;

    private final Timer timer;

    public Game() {
        next_move_square[0] = -1;
        next_move_square[1] = -1;
        setPreferredSize(new Dimension(WIDTH, HEIGHT));

        timer = new Timer(DELAY, this);
        timer.start();
    }
    @Override
    public void paintComponent(Graphics g) {

        super.paintComponent(g);

        drawBackground(g);

        // this smooths out animations on some systems
        Toolkit.getDefaultToolkit().sync();
    }

    private void drawBackground(Graphics g) {
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, WIDTH, HEIGHT);

        Graphics2D g2d = (Graphics2D) g;
        int width = 4;
        g2d.setStroke(new BasicStroke(width));

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                int x = i * WIDTH/3;
                int y = j * HEIGHT/3;
                g.setColor(Color.LIGHT_GRAY);
                g.drawLine(x + WIDTH/9, y, x + WIDTH/9, y + HEIGHT);
                g.drawLine(x + 2*WIDTH/9, y, x + 2*WIDTH/9, y + HEIGHT);

                g.drawLine(x, y + HEIGHT/9, x + WIDTH, y + HEIGHT/9);
                g.drawLine(x, y + 2*HEIGHT/9, x + WIDTH, y + 2*HEIGHT/9);
            }
        }

        g.setColor(Color.BLACK);
        g.drawLine(WIDTH/3, 0, WIDTH/3, HEIGHT);
        g.drawLine(2*WIDTH/3, 0, 2*WIDTH/3, HEIGHT);

        g.drawLine(0, HEIGHT/3, WIDTH, HEIGHT/3);
        g.drawLine(0, 2*HEIGHT/3, WIDTH, 2*HEIGHT/3);

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                int x = i * WIDTH/3;
                int y = j * HEIGHT/3;

                if (i == next_move_square[0] && j == next_move_square[1]) {
                    g2d.setStroke(new BasicStroke(6));
                    setColorForTeam(g, currentTeam);
                    g.drawLine(x, y, x + WIDTH/3, y); // top
                    g.drawLine(x, y, x, y + HEIGHT/3); // left
                    g.drawLine(x, y + HEIGHT/3, x + WIDTH/3, y + HEIGHT/3); // bottom
                    g.drawLine(x + WIDTH/3, y, x + WIDTH/3, y + HEIGHT/3); // right
                    g2d.setStroke(new BasicStroke(width));
                }

                if (semi_board[i][j] != 0) {
                    int padding = 10;
                    setColorForTeam(g, semi_board[i][j]);
                    int x1 = i * WIDTH/3;
                    int y1 = j * WIDTH/3;
                    if (semi_board[i][j] == 1) {
                        // draw x
                        drawXInSquare(g, x1+padding, y1+padding, WIDTH/3 - padding*2);
                    } else if (semi_board[i][j] == 2) {
                        // draw circle
                        drawCircleInSquare(g, x1+padding, y1+padding, WIDTH/3 - padding*2);
                    } else if (semi_board[i][j] == 3) {
                        // draw triangle
                        drawTriangleInSquare(g, x1+padding, y1+padding, WIDTH/3 - padding*2);
                    }
                } else {
                    for (int h = 0; h < 3; h++) {
                        for (int k = 0; k < 3; k++) {
                            int x1 = i * WIDTH/3 + h*WIDTH/9;
                            int y1 = j * WIDTH/3 + k*WIDTH/9;

                            int square = board[i][j][h][k];

                            drawTeamInSquare(g, i, j, h, k, square);

                            Point mousePosition = this.getMousePosition();

                            if (square == 0 && mousePosition != null) {
                                int mouseX = mousePosition.x;
                                int mouseY = mousePosition.y;
                                if (mouseX < x + WIDTH/3 && mouseX > x && mouseY > y && mouseY < y + HEIGHT/3) {
                                    if (mouseX < x1 + WIDTH/9 && mouseX > x1 && mouseY > y1 && mouseY < y1 + HEIGHT/9) {
                                        drawTeamInSquare(g, i, j, h, k, currentTeam);
                                    }
                                }
                            }

                        }
                    }
                }

            }
        }
    }

    public boolean makeMoveIfPossible(int i, int j, int h, int k) {
        int square = board[i][j][h][k];

        if (next_move_square[0] != -1 && (i != next_move_square[0] || j != next_move_square[1])) {
            return false;
        }

        if (square == 0) {
            board[i][j][h][k] = this.currentTeam;
            nextTeam();
            next_move_square[0] = h;
            next_move_square[1] = k;

            // check if this move won the square
            int winner = checkSquareWin(i, j);
            semi_board[i][j] = winner;
            System.out.println("WINNER: " + winner);

            // if h, k is already won, set the next move square to [-1, -1]
            if (semi_board[h][k] != 0) {
                next_move_square[0] = -1;
                next_move_square[1] = -1;
            }

            return true;
        }
        return false;
    }

    public int checkSquareWin(int i, int j) {
        int[][] sub_board = board[i][j];
        int size = sub_board.length;

        // Check rows
        for (int row = 0; row < size; row++) {
            if (sub_board[row][0] != 0 && allEqual(sub_board[row])) {
                return sub_board[row][0];
            }
        }

        // Check columns
        for (int col = 0; col < size; col++) {
            int firstCell = sub_board[0][col];
            if (firstCell != 0) {
                boolean columnWin = true;
                for (int row = 1; row < size; row++) {
                    if (sub_board[row][col] != firstCell) {
                        columnWin = false;
                        break;
                    }
                }
                if (columnWin) {
                    return firstCell;
                }
            }
        }

        // Check main diagonal
        int firstCell = sub_board[0][0];
        if (firstCell != 0) {
            boolean mainDiagonalWin = true;
            for (int k = 1; k < size; k++) {
                if (sub_board[k][k] != firstCell) {
                    mainDiagonalWin = false;
                    break;
                }
            }
            if (mainDiagonalWin) {
                return firstCell;
            }
        }

        // Check anti-diagonal
        firstCell = sub_board[0][size - 1];
        if (firstCell != 0) {
            boolean antiDiagonalWin = true;
            for (int k = 1; k < size; k++) {
                if (sub_board[k][size - 1 - k] != firstCell) {
                    antiDiagonalWin = false;
                    break;
                }
            }
            if (antiDiagonalWin) {
                return firstCell;
            }
        }

        // No win condition met
        return 0;
    }

    // Helper method to check if all elements in a row are the same
    private boolean allEqual(int[] array) {
        int first = array[0];
        for (int num : array) {
            if (num != first) {
                return false;
            }
        }
        return true;
    }

    @Override
    public void actionPerformed(ActionEvent e) {

        if (inputHandler.mouse_0_pressed) {
            inputHandler.mouse_0_pressed = false;
        }

        repaint();
    }


    @Override
    public void mouseClicked(MouseEvent e) {
        System.out.println(this.getMousePosition().x + ", " + this.getMousePosition().y);
        System.out.println("pressed");

        int mouseX = this.getMousePosition().x;
        int mouseY = this.getMousePosition().y;

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                int x = i * WIDTH/3;
                int y = j * HEIGHT/3;

                if (mouseX < x + WIDTH/3 && mouseX > x && mouseY > y && mouseY < y + HEIGHT/3) {

                    for (int h = 0; h < 3; h++) {
                        for (int k = 0; k < 3; k++) {
                            int x1 = i * WIDTH/3 + h*WIDTH/9;
                            int y1 = j * WIDTH/3 + k*WIDTH/9;

                            if (mouseX < x1 + WIDTH/9 && mouseX > x1 && mouseY > y1 && mouseY < y1 + HEIGHT/9) {
                                System.out.println("in square: " + i + ", " + j + ", " + h + ", " + k);
                                makeMoveIfPossible(i, j, h, k);
                            }
                        }
                    }
                }
            }
        }
    }

    public void setColorForTeam(Graphics g, int team) {
        if (team == 1) {
            g.setColor(Color.GREEN);
        } else if (team == 2) {
            g.setColor(Color.RED);
        } else if (team == 3) {
            g.setColor(Color.BLUE);
        }
    }

    public void drawTeamInSquare(Graphics g, int i, int j, int h, int k, int team) {

        int padding = 10;
        setColorForTeam(g, team);

        int x1 = i * WIDTH/3 + h*WIDTH/9;
        int y1 = j * WIDTH/3 + k*WIDTH/9;
        if (team == 1) {
            // draw x
            drawXInSquare(g, x1+padding, y1+padding, WIDTH/9 - padding*2);
        } else if (team == 2) {
            // draw circle
            drawCircleInSquare(g, x1+padding, y1+padding, WIDTH/9 - padding*2);
        } else if (team == 3) {
            // draw triangle
            drawTriangleInSquare(g, x1+padding, y1+padding, WIDTH/9 - padding*2);
        }
    }

    public void drawTriangleInSquare(Graphics g, int squareX, int squareY, int sideLength) {
        Graphics2D g2d = (Graphics2D) g;

        // Calculate the coordinates for the triangle vertices
        int x1 = squareX + sideLength / 2;        // Top vertex (centered horizontally)
        int y1 = squareY;                         // Top vertex (top of square)

        int x2 = squareX;                         // Bottom-left vertex (bottom left of square)
        int y2 = squareY + sideLength;

        int x3 = squareX + sideLength;            // Bottom-right vertex (bottom right of square)
        int y3 = squareY + sideLength;

        // Create the triangle as a polygon
        Polygon triangle = new Polygon();
        triangle.addPoint(x1, y1);
        triangle.addPoint(x2, y2);
        triangle.addPoint(x3, y3);

        // Draw the triangle
        g2d.drawPolygon(triangle);
    }

    public void drawXInSquare(Graphics g, int squareX, int squareY, int sideLength) {
        Graphics2D g2d = (Graphics2D) g;

        // Draw the first diagonal line (top-left to bottom-right)
        g2d.drawLine(squareX, squareY, squareX + sideLength, squareY + sideLength);

        // Draw the second diagonal line (top-right to bottom-left)
        g2d.drawLine(squareX + sideLength, squareY, squareX, squareY + sideLength);
    }

    public void drawCircleInSquare(Graphics g, int squareX, int squareY, int sideLength) {
        Graphics2D g2d = (Graphics2D) g;

        // Draw the circle
        g2d.drawOval(squareX, squareY, sideLength, sideLength);
    }

    public void nextTeam() {
        this.currentTeam += 1;
        if (this.currentTeam > 3) {
            this.currentTeam = 1;
        }
    }

    @Override
    public void mousePressed(MouseEvent e) {

    }

    @Override
    public void mouseReleased(MouseEvent e) {

    }

    @Override
    public void mouseEntered(MouseEvent e) {

    }

    @Override
    public void mouseExited(MouseEvent e) {

    }
}
