from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine(url="sqlite:///requests.db")
Session = sessionmaker(bind=engine)  

class Base(DeclarativeBase):
    pass

class ChatRequests(Base):  
    __tablename__ = "chat_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(index=True)
    prompt: Mapped[str]
    response: Mapped[str]

def get_user_requests(ip_address: str):
    with Session() as session:  
        query = select(ChatRequests).filter_by(ip_address=ip_address)
        result = session.execute(query)  
        return result.scalars().all() 

def add_request_data(ip_address: str, prompt: str, response: str) -> None:
    with Session() as session:
        new_request = ChatRequests(  
            ip_address=ip_address,
            prompt=prompt,
            response=response,
        )
        session.add(new_request)
        session.commit()