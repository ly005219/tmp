<template>
  <div>
    <div class="logo_img">
      <img src="@/assets/img/aboutUS.jpg" alt />
    </div>
    <div class="introduce_content">
      <div class="introduce_item">
        <label>电话：</label>
        <p>13333333333</p>
      </div>
      <div class="introduce_item">
        <label>公司地址：</label>
        <p>北京尚学堂</p>
      </div>
      <div class="introduce_item">
        <label>问题反馈：</label>
        <p>133333333333@qq.com</p>
      </div>
      <div class="introduce_item">
        <label>商业合作：</label>
        <p>13333333333</p>
      </div>
    </div>
    <div class="introduce_foot">Copyright@2020-2050 Godfy. All Rights Reserved</div>
  </div>
</template>

<style lang="less" >
.logo_img {
  width: 100%;
  height: 200px;
  img {
    width: 100%;
    height: 100%;
  }
}
.introduce_content {
  width: 100%;
  height: 250px;
  .introduce_item {
    width: 100%;
    height: 60px;
    margin-top: 5px;
  }
}
.introduce_foot {
  position: fixed;
  bottom: 54px;
  width: 100%;
  height: 20px;
  font-size: 14px;
  text-align: center;
  line-height: 20px;
  color: gray;
}
</style>

<script>
export default {
  data: function() {
    return {};
  },
  mounted() {
    var header_title = document.getElementsByClassName("mint-header-title")[0];
    header_title.innerText = "关于我们"
  }
};
</script>