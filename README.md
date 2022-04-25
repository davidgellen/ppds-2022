# Assignment 9
Create a simple application using CUDA.
The implementation is based on lecture https://www.youtube.com/watch?v=5DFS6Mgh8CU by Mgr. Ing. Matúš Jókay, PhD. and from website https://uim.fei.stuba.sk/i-ppds/9-cvicenie-cuda-pomocou-numba/.

### Application concept
Application loads an image. Then it runs an algorithm known as mean adaptive thresholding. This algorithm iterates through an image with a grid of size n x n and calculates the average pixel value of the area represented by the grid. If the current pixel value is greater than the area average, if sets the pixel value to 255, otherwise to 0.

We decided to have a grid of size 15 x 15 since smaller grids weren't producing desired results. However, results may differ picture to picture.
### Host:
```
image = Image.open('image.png')
data = numpy.asarray(Image.open('image.png'))
data_final = numpy.asarray(Image.open('image.png'))
threads_per_block = (20, 20)
blocks_per_grid_x = math.ceil(data.shape[0] / threads_per_block[0])
blocks_per_grid_y = math.ceil(data.shape[1] / threads_per_block[1])
blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
adaptive_thresholding[blocks_per_grid, threads_per_block](data, data_final)
Image.fromarray(data_final).save("result.png")
```

### Kernel:
```
@cuda.jit
def adaptive_thresholding(data_orig, data_result):
    x, y = cuda.grid(2)
    x_max, y_max = data_orig.shape
    if x < x_max and y < y_max:
        sum = 0
        for i in range(15):
            for j in range(15):
                sum += data_orig[x - 7 + i][y - 7 + j]
        average = sum / 225
        if data_orig[x][y] > average:
            data_result[x][y] = 255
        else:
            data_result[x][y] = 0
```


file: program.py

### Results

##### Original image

![Alt text](image.png?raw=true "Original")

##### After adaptive thresholding

![Alt text](result.png?raw=true "Result")
