<template>
  <main class="container">
    <div class="row mb-4">
      <div class="col-md-6 order-md-2 text-left">
        <div class="text-center">
          <h3 class="featurette-heading">春季型人</h3>
        </div>
        <p>☆ 春季型人具備自然的春天所帶來的美好特質，例如：生機、活潑、明媚。</p>
        <p>
          ☆
          他們皮膚明亮，眼神閃耀、光潔，是生活中最具快樂和靚麗的一族，正如大自然春天帶給我們的欣悅一般，春季型人是朝氣而充滿活力的。
        </p>
        <p>☆ 適合高明亮、高飽和、生動且清新的色系，像是俏皮的春季花卉色調。</p>
        <p>☆ 黃色是首選，帶有淡黃色調的象牙白、橘紅色、略帶黃色的淺藍色等，都是不錯的選擇。</p>
        <p>☆ 盡量避免穿黑色，過深過重的顏色會蓋著自己的光芒，也襯托不出春季型人的俏麗和光彩。</p>
        <p>☆ 飾品類適合光澤明亮的黃金飾品。</p>
        <p>☆ 若搭配了適合的顏色：</p>
        <p>&emsp;&ensp;✓ 臉部變得明亮</p>
        <p>&emsp;&ensp;✓ 可呈現出血色感</p>
        <p>&emsp;&ensp;✓ 看起來彈力有光澤、生氣蓬勃</p>
      </div>
      <div class="col-md-6 order-md-1">
        <img src="@/assets/img/spring_person.jpeg" class="img-fluid rounded" alt="春季型明星" />
      </div>
    </div>

    <section class="text-center">
      <h3>適合的色彩</h3>
      <table class="table table-bordered color-table">
        <tbody>
          <tr>
            <td style="background-color: #f7d0c3"></td>
            <td style="background-color: #ec7c88"></td>
            <td style="background-color: #f2993f"></td>
            <td style="background-color: #a9cf60"></td>
            <td style="background-color: #a2d7db"></td>
            <td style="background-color: #3a548f"></td>
            <td style="background-color: #e6c88c"></td>
          </tr>
          <tr>
            <td style="background-color: #f9c498"></td>
            <td style="background-color: #e9636e"></td>
            <td style="background-color: #ffed53"></td>
            <td style="background-color: #80bf4a"></td>
            <td style="background-color: #989dba"></td>
            <td style="background-color: #914a8c"></td>
            <td style="background-color: #d8ae64"></td>
          </tr>
          <tr>
            <td style="background-color: #ed7b63"></td>
            <td style="background-color: #e64861"></td>
            <td style="background-color: #f6d963"></td>
            <td style="background-color: #2fa73b"></td>
            <td style="background-color: #8099b8"></td>
            <td style="background-color: #fef0c3"></td>
            <td style="background-color: #efb31c"></td>
          </tr>
          <tr>
            <td style="background-color: #ec5621"></td>
            <td style="background-color: #e6251c"></td>
            <td style="background-color: #e0cfc7"></td>
            <td style="background-color: #4eb8ae"></td>
            <td style="background-color: #016ea9"></td>
            <td style="background-color: #fdeeab"></td>
            <td style="background-color: #905324"></td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Add the "重新測驗" button here -->
    <div class="text-center retest-button">
      <button @click="goToRetest" class="btn btn-primary mt-3">重新測驗</button>
    </div>
  </main>
</template>

<script>
export default {
  name: 'color_detail',
  methods: {
    goToRetest() {
      this.$router.push({ name: 'color_retest' }); // Assuming the route name is 'color_retest'
    }
  }
};
</script>

<style scoped>
/* Add main content specific styles here */
.container {
  margin-top: 15px;
  margin-bottom: 30px;
}

.text-center {
  color: #917b56;
  text-shadow: 2px 2px 4px rgba(127, 125, 125, 0.4);
  text-align: center;
  justify-content: center;
  align-items: center;
  padding-bottom: 15px;
}

.text-left p {
  font-size: 16px;
  font-weight: 350;
  margin-right: 7%;
}

.color-table {
  width: 100%;
  margin: 20px 0;
  border-collapse: separate;
  border-spacing: 10px;
  padding-bottom: 50px;
}
.color-table td {
  width: 50px;
  height: 50px;
  border-radius: 10px;
}
/* 调整图片的容器和图片样式 */
.col-md-6.order-md-1 {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
}

.col-md-6.order-md-1 img {
  max-width: 100%;
  height: auto;
  object-fit: cover;
  margin-top: 20px;
  margin-bottom: 20px;
}

.retest-button {
  margin-top: -40px; /* 调整此值以控制按钮与上方元素之间的距离 */
}

/* 小屏幕下调整图片样式 */
@media (max-width: 768px) {
  .col-md-6.order-md-1 {
    text-align: center;
  }

  .col-md-6.order-md-1 img {
    max-width: 80%;
    margin-top: 10px;
  }
}

</style>
