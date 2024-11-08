import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;


public class InputHandler implements KeyListener, MouseListener {
    public boolean mouse_0_pressed = false;
    public boolean mouse_1_pressed = false;

    @Override
    public void keyTyped(KeyEvent e) {

    }

    @Override
    public void keyPressed(KeyEvent e) {

    }

    @Override
    public void keyReleased(KeyEvent e) {

    }

    @Override
    public void mouseClicked(MouseEvent e) {
        this.mouse_1_pressed = true;
    }

    @Override
    public void mousePressed(MouseEvent e) {
        this.mouse_0_pressed = true;
    }

    @Override
    public void mouseReleased(MouseEvent e) {
        this.mouse_0_pressed = false;
    }

    @Override
    public void mouseEntered(MouseEvent e) {

    }

    @Override
    public void mouseExited(MouseEvent e) {

    }
}
