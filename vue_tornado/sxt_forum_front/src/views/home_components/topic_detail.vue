 <template>
  <div class="abc">
    <div class="d-nav">
      <div class="d-option" @click="$router.back(-1)">返回</div>
      <div class="d-name">{{topic.user.nick_name}}</div>
      <div class="btn" v-if="flag == false" @click="addFriend">关注</div>
      <div class="btn" v-if="flag == true" @click="deleteFriend">取消关注</div>
    </div>
    <div class="mui-scroll-wrapper scrollstyle">
      <div class="mui-scroll">
        <div class="detail">
          <div class="d-img" v-if="topic.imgs != ''">
            <mt-swipe>
              <mt-swipe-item v-for="item in topic.imgs" :key="item.id">
                <img
                  class="txt-img"
                  preview="1"
                  :preview-text="topic.title"
                  v-lazy="'http://localhost:8000'+item"
                  alt
                />
              </mt-swipe-item>
            </mt-swipe>
          </div>
          <div class="d-main">
            <div class="d-title">{{topic.title}}</div>
            <div class="d-txt">{{topic.content}}</div>
            <div class="Disclaimer">免责声明：本文章来自客户端自媒体，不代表本平台的观点和立场！</div>
            <div class="d-time">{{topic.created_time | dateFormat}}</div>
            <div class="d-tag">{{topic.type_}}</div>
          </div>
          <div class="like_btn_content">
            <div class="like_content_explain">喜欢！那就点击收藏吧！</div>
            <div class="like_img" @click="collection">
              <img src="../../assets/icon/like_icon.png" alt />
            </div>
          </div>
          <div class="comment">
            <div class="comment_head">评论：{{comments.length}}</div>
            <div class="comment_text">
              <input ref="textarea" placeholder="请输入你要评论的内容" maxlength="120" />
              <button class="comment_btn" @click="commitComment">发表评论</button>
            </div>
            <div class="comment_content" v-for="(comment,index) in comments" :key="comment.id">
              <div class="comment_content_head">
                <div class="commenter_avatar">
                  <img :src="'http://localhost:8000'+comment.user.pic" alt />
                </div>
                <div class="commenter_nickname">{{comment.user.nick_name}}</div>
                <div class="commenter_floor">{{index+1}}楼</div>
              </div>
              <div class="commenter_content">
                <div class="content">{{comment.content}}</div>
              </div>
              <div class="comment_footer">
                <div class="comment_createdtime">{{comment.create_time | dateFormat }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>
<style lang="less">
.mui-scroll-wrapper {
  background: white;
  overflow:scroll!important;
}
.mint-swipe {
  border-radius: 10px;
  height: 300px;
  margin: 8px;
  border: none;
  box-shadow: 0px 0px 10px -10px black;
  .mint-swipe-item {
    img {
      width: 100%;
      height: 100%;
      background-size: cover;
    }
  }
}
.scrollstyle {
  margin-top: 50px;
}
.abc {
  // height: 100%;
}
.d-nav {
  background-color: white;
  height: 50px;
  width: 100%;
  position: fixed;
  z-index: 999;
  top: 0px;
  .d-option {
    width: 30px;
    height: 30px;
    margin: 10px;
    // overflow: hidden;
    float: left;
    line-height: 30px;
    font-size: 15px;
    img {
      width: 100%;
    }
  }
  .d-name {
    padding-left: 55px;
    width: 230px;
    float: left;
    height: 50px;
    color: black;
    font-size: 17px;
    line-height: 50px;
    text-align: center;
    // overflow: hidden;
  }
  .btn {
    width: 70px;
    float: right;
    height: 30px;
    line-height: 30px;
    margin: 10px;
    color: rgb(255, 66, 66);
    font-size: 14px;
    text-align: center;
    border: 1px solid rgb(255, 66, 66);
    border-radius: 25px;
  }
}
.detail {
  margin-bottom: 50px;
  background-color: white;
  width: 100%;
  // height: 100%;
  .d-img {
    width: 100%;
    .swiper-item img {
      width: 100%;
      height: 550px;
      background-size: auto;
    }
    .swiper-item img[lazy="loading"] {
      width: 100%;
    }
    .swiper-pagination-fraction {
      width: 20%;
      left: 80%;
    }
  }
  .d-main {
    width: 100%;
    margin-top: 5px;
    .d-title {
      padding-left: 8px;
      width: 100%;
      line-height: 30px;
      font-size: 17px;
      font-weight: bold;
      color: black;
    }
    .d-txt {
      padding: 8px;
      width: 100%;
      font-size: 14px;
      color: rgb(80, 80, 80);
      font-weight: normal;
    }
    .Disclaimer {
      margin-left: 10px;
      width: 100%;
      color: gray;
      font-size: 10px;
    }
    .d-tag {
      height: 30px;
      width: 80px;
      line-height: 30px;
      text-align: center;
      background-color: pink;
      border: none;
      border-radius: 15px;
      font-size: 12px;
      color: rgb(100, 100, 255);
      line-height: 30px;
      margin-left: 10px;
    }
    .d-time {
      margin-left: 10px;
      font-size: 8px;
      color: gray;
      background-color: transparent;
    }
  }
  .like_btn_content {
    width: 100%;
    height: 100px;
    .like_content_explain {
      width: 100%;
      text-align: center;
      margin-top: 10px;
    }
    .like_img {
      width: 100%;
      height: 100%;
      position: relative;
      img {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 50px;
        height: 50px;
      }
    }
  }
}
.comment {
  margin-top: 10px;
  width: 100%;
  .comment_text {
    width: 100%;
    height: 40px;
    margin-top: 5px;
    input {
      float: left;
      width: 80%;
      margin: 0;
      height: 40px;
      border: 1px solid gray;
    }
    .comment_btn {
      float: left;
      width: 20%;
      height: 40px;
      color: black;
      border: 1px solid gray;
    }
  }
  .comment_head {
    width: 100%;
    height: 40px;
    line-height: 40px;
    background: white;
    color: black;
    font-weight: 900;
    padding-left: 10px;
  }
  .comment_content {
    width: 100%;
    margin-top: 5px;
    background: white;
    .comment_content_head {
      width: 100%;
      height: 30px;
      .commenter_avatar {
        float: left;
        width: 30px;
        height: 30px;
        margin-left: 20px;
        img {
          width: 100%;
          height: 100%;
          border-radius: 50%;
        }
      }
      .commenter_nickname {
        float: left;
        width: 50%;
        height: 30px;
        margin-left: 10px;
        line-height: 30px;
        font-size: 15px;
        color: rgb(243, 159, 4);
      }
      .commenter_floor {
        float: right;
        font-size: 10px;
        font-weight: 100;
        line-height: 30px;
        margin-right: 10px;
      }
    }
    .commenter_content {
      width: 100%;
      .content {
        width: 80%;
        margin-left: 60px;
      }
    }
    .comment_footer {
      width: 100%;
      .comment_createdtime {
        width: 80%;
        margin-left: 60px;
        font-size: 10px;
        font-weight: 100;
        color: gray;
      }
    }
  }
}
</style>
<script>
import mui from "@/../lib/mui/js/mui.js";
import myaxios, {
  gettopicById,
  getcomment,
  commitComment,
  addFriendURL,
  judgeFriendURL,
  deleteFriendURL,
  getsessionURL,
  addCollectionURL
} from "@/tools/myaxios.js";
import { Toast } from "mint-ui";
import { async } from "q";
import { EALREADY } from "constants";
export default {
  data: function() {
    return {
      user: "",
      topic: "",
      comments: "",
      flag: ""
    };
  },
  methods: {
    async commitComment() {
      var comment_content = this.$refs.textarea.value;
      var topic_id = this.$route.params.id;
      var obj = {
        content: comment_content,
        topic_id: topic_id
      };
      if (comment_content) {
        var result = await myaxios("POST", commitComment, obj);
        if (result.data.code == 401) {
          this.$router.push("/login");
          Toast(result.data.msg);
        } else if (result.data.code  == 200) {
          Toast(result.data.msg);
          this.$refs.textarea.value = "";
          var obj2 = {
            id: this.$route.params.id
          };
          var result2 = await myaxios("POST", getcomment, obj2);
          if (result2.data.code  == 200) {
            this.comments = result2.data.comments;
        
          } else {
            Toast("请求出错请重试！");
          }
        } else {
          Toast(result.data.msg);
        }
      } else {
        Toast("评论的内容不能为空哦！！！");
      }
    },
    async collection() {
        var obj = {
          id: this.topic.id,
        };
        var result2 = await myaxios("POST", addCollectionURL, obj);
        if (result2.data.code  == 200) {
          Toast(result2.data.msg);
        } else if (result2.data.code == 500) {
          Toast(result2.data.msg);
        }else if(result2.data.code == 401){
          this.$router.push("/login");
        }
    },
    async addFriend() {
      var friendID = this.topic.user.id;
      var obj = {
        id: friendID
      };
      var result = await myaxios("POST", addFriendURL, obj);
      if (result.data.code  == 200) {
        Toast("关注成功！");
        var obj = {
          id: this.topic.user.id
        };
        var result2 = await myaxios("POST", judgeFriendURL, obj);
        if (result2.data.code  == 200) {
          this.flag = result2.data.flag;
        }
      } else if(result.data.code  == 500) {
        Toast("关注失败！");
      }
      else if(result.data.code  == 401){
        this.$router.push("/login");
        Toast(result.data.msg);
      }
    },
    async deleteFriend() {
      var obj = {
        id: this.topic.user.id
      };
      var result = await myaxios("DELETE", deleteFriendURL, obj);
      if (result.data.code  == 200) {
        Toast("取消关注成功！");
        this.flag = false;
      }
    }
  },
  async created() {
    var obj = {
      id: this.$route.params.id
    };
    var result = await myaxios("POST", gettopicById, obj);
    if (result.data.code == 200) {
      this.topic = result.data.topic;
    } else {
      Toast("请求出错请重试！");
    }
    var result2 = await myaxios("POST", getcomment, obj);
    if (result2.data.code  == 200) {
      this.comments = result2.data.comments;
    } else {
      Toast("请求出错请重试！");
    }
    var obj2 = {
      id: this.topic.user.id
    };
    var result3 = await myaxios("POST", judgeFriendURL, obj2);
    if (result3.data.code  == 200) {
      this.flag = result3.data.flag;
    }
  },
  mounted() {
    mui(".mui-scroll-wrapper").scroll({
      deceleration: 0.0005 //flick 减速系数，系数越大，滚动速度越慢，滚动距离越小，默认值0.0006
    });
  }
};
</script>
