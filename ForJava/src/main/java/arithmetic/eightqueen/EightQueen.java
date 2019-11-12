package arithmetic.eightqueen;

import java.util.Arrays;

/**
 * @author skdtd
 * @date 2019/11/11 22:27
 */
public class EightQueen {
    /**
     * 8个皇后
     */
    private int max = 8;
    private int[] map = new int[max];
    private static int count = 0;
    public void check(int n) {
        if (n == 8) {
            System.out.println(++count + ":\t" + Arrays.toString(map));
            return;
        }

        for (int i = 0; i < max; i++) {
            map[n] = i;
            if (finding(n)) {
                check(n + 1);
            }
        }
    }

    private boolean finding(int n) {
        for (int i = 0; i < n; i++) {
            if (map[i] == map[n] || Math.abs(n - i) == Math.abs(map[n] - map[i])) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        EightQueen e = new EightQueen();
        e.check(0);
    }
}
