import functools
import jwt

from config import secret, jwt_exp
from manager import manager
from manager.models import User

def login_required_async(func):
    @functools.wraps(func)
    async def wrapper(self,*arg,**kwargs):
        # 验证用户是否登录
        # 获取token
        token = self.request.headers.get('token')
        if not token:
            self.finish({'msg':'请先登录，缺少token','code':401})
            return
            
        try:
            # 确保token是bytes类型
            if isinstance(token, str):
                token = token.encode('utf-8')
                
            # 从token值中解析出email
            payload = jwt.decode(token, secret, options={'verify_exp':True}, algorithms=["HS256"], leeway=jwt_exp)
            
            if payload:
                # 通过email查询数据
                email = payload.get('email')
                try:
                    user = await manager.get(User, email=email)
                    self._user_email = email
                    self._user_id = user.id
                    # 登录了,运行func()
                    await func(self,*arg,**kwargs)
                except Exception as e:
                    print(f"用户查询错误: {e}")
                    self.finish({'msg':'用户验证失败','code':401})
            else:
                # 没有payload，回馈请登录
                self.finish({'msg':'无效的令牌','code':401})
        except jwt.exceptions.DecodeError as e:
            print(f"JWT解码错误: {e}")
            self.finish({'msg':'无效的令牌格式','code':401})
        except jwt.exceptions.ExpiredSignatureError:
            self.finish({'msg':'令牌已过期','code':401})
        except Exception as e:
            print(f"其他错误: {e}")
            self.finish({'msg':'认证过程发生错误','code':500})
    return wrapper