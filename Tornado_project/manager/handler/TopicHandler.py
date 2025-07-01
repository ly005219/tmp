from manager import manager
from manager.handler.BaseHandler import BaseHandler
from manager.models import TopicModel
from manager.wtforms import AddTopicForm
from manager.models import User
from manager.decorators import login_required_async
from config import settings
from uuid import uuid4
import os




class GetManyTopicHandler(BaseHandler):
    async def get(self):
        # 从数据库中获取数据
        topics = await manager.execute(TopicModel.select().order_by(TopicModel.create_time.desc()))
        rs_data = {}
        data = []
        for topic in topics:
            # 把文章信息转成json
            t=tran_topic(topic)
            # 增加返回评论数
            t['comment_num'] = topic.comments.count()
            # 增加返回收藏数
            t['like_num'] = topic.collections.count()

            data.append(t)
        rs_data['code']=200
        rs_data['msg']='获取成功'
        rs_data['topics'] = data
        self.finish(rs_data)
    async def post(self):
        # 从前端获取传递来的过滤类型
        type_ = self.get_body_argument('type')
            # 从数据库中获取数据
        topics = await manager.execute(TopicModel.select().where(TopicModel.type_ == type_).order_by(TopicModel.create_time.desc()))
        rs_data = {}
        data = []
        for topic in topics:
            # 将topic对象转成json数据
            t=tran_topic(topic)
            # # 增加返回评论数
            # t['comment_num'] = topic.comments.count()
            # # 增加返回收藏数
            # t['like_num'] = topic.collections.count()
            data.append(t)
        rs_data['code']=200
        rs_data['msg']='获取成功'
        rs_data['topics'] = data
        self.finish(rs_data)


class GetOneTopicHandler(BaseHandler):
    async def post(self):
        id=self.get_argument('id')
        topic = await manager.get(TopicModel,id=id)
        if topic:
            t=tran_topic(topic)
            # 增加返回评论数
            t['comment_num'] = topic.comments.count()
            # 增加返回收藏数
            t['like_num'] = topic.collections.count()
           
            rs_data = {}
            rs_data['code'] = 200
            rs_data['msg'] = '获取成功'
            rs_data['topic'] = t
            self.finish(rs_data)
          
         
        else:
            rs_data = {}
            rs_data['code'] = 404
            rs_data['msg'] = '文章不存在'

def tran_topic(topic):
      # 把文章信息转成json
            t = topic.to_json()
            # 把用户信息转成json
            t['user'] = t.get('user').to_json()
            # 分割图片的地址
            if t.get('imgs')==None or t.get('imgs') == '' :
                t['imgs'] = None
            else:
                t['imgs'] = t.get('imgs').split(',')
            return t


class AddTopicHandler(BaseHandler):
    @login_required_async
    async def post(self):
        rs_data ={}
        # 获取传递的数据,传递到Form
        topic_form = AddTopicForm(self.request.arguments)
        # 验证
        if topic_form.validate():
            # 验证成功，增加
            # 获取当前用户信息
            user = await manager.get(User,id =self._user_id)
            # 生成一个唯一的ID
            id = uuid4().hex
            # 建立一个full_img_path
            img_path = []
            # 保存图片
            imgs = self.request.files.get('imgs',[])
            for i in imgs:
                # 获取文件名字
                file_name = f'{uuid4().hex}{os.path.splitext(i.get("filename"))[-1]}'
                # 获取文件全名
                full_path = os.path.join(settings.get('static_path'),'img',file_name)
                # 保存文件
                with open(full_path,'wb') as f:
                    f.write(i.get('body'))
                # 追加图片的路径到img_path
                img_path.append(f'/static/img/{file_name}')
            # 更新到topic对象里面去
            await manager.create(TopicModel,**topic_form.data, user = user,id = id,imgs=','.join(img_path))
            rs_data['code'] =200
            rs_data['msg'] = '发帖成功！'
        else:
            # 验证失败，数据不合法
            rs_data['code'] =500
            rs_data['msg'] = '发帖失败！'
        self.finish(rs_data)

class GetMyTopicHandler(BaseHandler):
    @login_required_async
    async def post(self):
        rs_data = {}
        # 通过user_id进行筛选获取帖子信息
        # topics = await manager.execute(TopicModel.select().where(TopicModel.user.id == self._user_id).order_by(TopicModel.create_time.desc())) 不能用
        topics = await manager.execute(TopicModel.select().join(User).where(User.id == self._user_id).order_by(TopicModel.create_time.desc()))
        # 将所有帖子信息转换成json<包含user信息>
        data = []
        for t in topics:
            d = tran_topic(t)
            data.append(d)
        # 响应前端
        rs_data['code'] = 200
        rs_data['msg'] ='获取个人帖子信息成功！'
        rs_data['topics'] = data
        self.finish(rs_data)

# 新增热门帖子处理器
class GetHostPostHandler(BaseHandler):
    async def get(self):
        # 获取点击量最多的帖子作为热门帖子
        topics = await manager.execute(TopicModel.select().order_by(TopicModel.chick_num.desc()).limit(10))
        rs_data = {}
        data = []
        for topic in topics:
            # 把文章信息转成json
            t = tran_topic(topic)
            # 添加额外信息
            user = await manager.get(User, id=topic.user_id)
            t['nickname'] = user.nick_name if user.nick_name else user.email
            t['icon'] = user.pic
            
            # 确保有img字段，从imgs中获取第一张图片
            if t.get('imgs') and isinstance(t.get('imgs'), list) and len(t.get('imgs')) > 0:
                t['img'] = t.get('imgs')[0]
            else:
                t['img'] = '/static/img/default.jpg'
                
            data.append(t)
        rs_data['code'] = 200
        rs_data['msg'] = '获取热门帖子成功'
        rs_data['topics'] = data
        self.finish(rs_data)

# 新增搜索处理器
class SearchTopicHandler(BaseHandler):
    async def post(self):
        # 获取搜索关键词
        search_content = self.get_body_argument('searchContent', '')
        
        if not search_content:
            self.finish({'code': 400, 'msg': '搜索内容不能为空'})
            return
            
        # 搜索标题或内容包含关键词的帖子
        topics = await manager.execute(
            TopicModel.select().where(
                (TopicModel.title.contains(search_content)) | 
                (TopicModel.content.contains(search_content))
            ).order_by(TopicModel.create_time.desc())
        )
        
        rs_data = {}
        data = []
        for topic in topics:
            # 把文章信息转成json
            t = tran_topic(topic)
            # 添加额外信息
            user = await manager.get(User, id=topic.user_id)
            t['nickname'] = user.nick_name if user.nick_name else user.email
            t['icon'] = user.pic
            data.append(t)
            
        rs_data['code'] = 200
        rs_data['msg'] = '搜索成功'
        rs_data['topics'] = data
        self.finish(rs_data)

# 新增轮播图数据处理器
class GetLunboDataHandler(BaseHandler):
    async def get(self):
        # 获取最新的5条帖子作为轮播图数据
        topics = await manager.execute(TopicModel.select().order_by(TopicModel.create_time.desc()).limit(5))
        rs_data = {}
        data = []
        for topic in topics:
            # 转换成json数据以提取所需信息
            topic_json = tran_topic(topic)
            
            # 只需要id和第一张图片
            t = {}
            t['_id'] = topic.id
            # 取第一张图片作为轮播图
            if topic_json.get('imgs') and isinstance(topic_json.get('imgs'), list) and len(topic_json.get('imgs')) > 0:
                t['img'] = topic_json.get('imgs')[0]
            else:
                t['img'] = '/static/img/default.jpg'
            data.append(t)
            
        rs_data['code'] = 200
        rs_data['msg'] = '获取轮播图数据成功'
        rs_data['lunboData'] = data
        self.finish(rs_data)