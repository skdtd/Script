package structure.sparsearray;


/**
 * 稀疏压缩解压缩
 *
 * @author skdtd
 * @date 2019/11/7 19:29
 */
public class SparseKit {

    public int[][] compress(int[][] arr, int valueType) {
        // int[0][] 用来存二位数组格局
        // int[1][] 用来存row
        // int[2][] 用来存col
        // int[3][] 用来存value
        int[][] compressArr = new int[3][];

        // 保存初始化格局
        compressArr[0][0] = arr.length;
        compressArr[0][1] = arr[0].length;
        compressArr[0][2] = valueType;

        // 创建计数器
        int count = 1;
        // 开始转换
        for (int i = 0; i < arr.length; i++) {
            for (int j = 0; j < arr[i].length; j++) {
                int v = arr[i][j];
                if (v != 0) {
                    compressArr[count][0] = i;
                    compressArr[count][1] = j;
                    compressArr[count++][2] = v;
                }
            }
        }
        return compressArr;
    }

    public int[][] uncompress(int[][] arr) {
        // 判断参数有效性
        if (arr.length != 3 && arr[0].length != 3) {
            System.err.println("数据格式不正确");
            return null;
        }

        // 初始化格局
        int row = arr[0][0];
        int col = arr[0][1];
        int[][] uncompressArr = new int[row][col];

        // 开始转换
        for (int[] data : arr) {
            uncompressArr[data[0]][data[1]] = data[2];
        }
        return uncompressArr;
    }
}