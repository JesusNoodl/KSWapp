from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, DateTime, Double, ForeignKeyConstraint, Identity, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, Table, Text, Time, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import uuid

class Base(DeclarativeBase):
    pass


class Address(Base):
    __tablename__ = 'address'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='address_pkey'),
        UniqueConstraint('id', name='address_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    house_number: Mapped[Optional[int]] = mapped_column(Integer)
    house_name: Mapped[Optional[str]] = mapped_column(Text)
    street_name: Mapped[Optional[str]] = mapped_column(Text)
    town: Mapped[Optional[str]] = mapped_column(Text)
    post_code: Mapped[Optional[str]] = mapped_column(Text)
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    contact: Mapped[List['Contact']] = relationship('Contact', back_populates='address')
    location: Mapped[List['Location']] = relationship('Location', back_populates='address')


class AgeCategory(Base):
    __tablename__ = 'age_category'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='age_category_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    cat_name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    person: Mapped[List['Person']] = relationship('Person', back_populates='age_category')
    age_category_XREF: Mapped[List['AgeCategoryXREF']] = relationship('AgeCategoryXREF', back_populates='age_category')


class Belt(Base):
    __tablename__ = 'belt'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='belt_pkey'),
        UniqueConstraint('id', name='belt_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    is_stripe: Mapped[bool] = mapped_column(Boolean)
    korean_name: Mapped[str] = mapped_column(Text)
    primary_colour: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    person: Mapped[List['Person']] = relationship('Person', back_populates='belt_level')
    promotions: Mapped[List['Promotions']] = relationship('Promotions', back_populates='belt')


class EventType(Base):
    __tablename__ = 'event_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='event_type_pkey'),
        UniqueConstraint('id', name='event_type_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    event: Mapped[List['Event']] = relationship('Event', back_populates='event_type')


t_full_person = Table(
    'full_person', Base.metadata,
    Column('first_name', Text),
    Column('last_name', Text),
    Column('student_id', Text),
    Column('dob', DateTime(True)),
    Column('active', Boolean),
    Column('black_belt_id', Text),
    Column('role', String),
    Column('belt_name', Text),
    Column('korean_belt_name', Text),
    Column('age_category', String)
)


t_location_adress = Table(
    'location_adress', Base.metadata,
    Column('title', String),
    Column('house_number', Integer),
    Column('house_name', Text),
    Column('street_name', Text),
    Column('town', Text),
    Column('post_code', Text)
)


class News(Base):
    __tablename__ = 'news'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='news_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    body: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('now()'))
    published_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


t_pg_stat_statements = Table(
    'pg_stat_statements', Base.metadata,
    Column('userid', OID),
    Column('dbid', OID),
    Column('toplevel', Boolean),
    Column('queryid', BigInteger),
    Column('query', Text),
    Column('plans', BigInteger),
    Column('total_plan_time', Double(53)),
    Column('min_plan_time', Double(53)),
    Column('max_plan_time', Double(53)),
    Column('mean_plan_time', Double(53)),
    Column('stddev_plan_time', Double(53)),
    Column('calls', BigInteger),
    Column('total_exec_time', Double(53)),
    Column('min_exec_time', Double(53)),
    Column('max_exec_time', Double(53)),
    Column('mean_exec_time', Double(53)),
    Column('stddev_exec_time', Double(53)),
    Column('rows', BigInteger),
    Column('shared_blks_hit', BigInteger),
    Column('shared_blks_read', BigInteger),
    Column('shared_blks_dirtied', BigInteger),
    Column('shared_blks_written', BigInteger),
    Column('local_blks_hit', BigInteger),
    Column('local_blks_read', BigInteger),
    Column('local_blks_dirtied', BigInteger),
    Column('local_blks_written', BigInteger),
    Column('temp_blks_read', BigInteger),
    Column('temp_blks_written', BigInteger),
    Column('blk_read_time', Double(53)),
    Column('blk_write_time', Double(53)),
    Column('temp_blk_read_time', Double(53)),
    Column('temp_blk_write_time', Double(53)),
    Column('wal_records', BigInteger),
    Column('wal_fpi', BigInteger),
    Column('wal_bytes', Numeric),
    Column('jit_functions', BigInteger),
    Column('jit_generation_time', Double(53)),
    Column('jit_inlining_count', BigInteger),
    Column('jit_inlining_time', Double(53)),
    Column('jit_optimization_count', BigInteger),
    Column('jit_optimization_time', Double(53)),
    Column('jit_emission_count', BigInteger),
    Column('jit_emission_time', Double(53))
)


t_pg_stat_statements_info = Table(
    'pg_stat_statements_info', Base.metadata,
    Column('dealloc', BigInteger),
    Column('stats_reset', DateTime(True))
)


class Role(Base):
    __tablename__ = 'role'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='role_pkey'),
        UniqueConstraint('id', name='role_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('now()'))
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    person: Mapped[List['Person']] = relationship('Person', back_populates='role')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        {'comment': 'Profile data for each user.'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, comment='References the internal Supabase Auth user.')
    role: Mapped[str] = mapped_column(Text, server_default=text("'user'::text"))
    email: Mapped[Optional[str]] = mapped_column(Text)

    contact: Mapped[List['Contact']] = relationship('Contact', back_populates='user')
    user_person: Mapped[List['UserPerson']] = relationship('UserPerson', back_populates='user')


class Contact(Base):
    __tablename__ = 'contact'
    __table_args__ = (
        ForeignKeyConstraint(['address_id'], ['address.id'], name='contact_address_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='contact_user_id_fkey'),
        PrimaryKeyConstraint('id', name='contact_pkey'),
        UniqueConstraint('id', name='contact_id_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    is_primary: Mapped[bool] = mapped_column(Boolean)
    first_name: Mapped[str] = mapped_column(Text)
    second_name: Mapped[str] = mapped_column(Text)
    primary_phone_number: Mapped[int] = mapped_column(BigInteger)
    relation: Mapped[str] = mapped_column(Text)
    address_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    secondary_phone_number: Mapped[Optional[int]] = mapped_column(BigInteger)
    email: Mapped[Optional[str]] = mapped_column(Text)

    address: Mapped['Address'] = relationship('Address', back_populates='contact')
    user: Mapped['Users'] = relationship('Users', back_populates='contact')


class Person(Base):
    __tablename__ = 'person'
    __table_args__ = (
        ForeignKeyConstraint(['age_category_id'], ['age_category.id'], name='person_age_category_id_fkey'),
        ForeignKeyConstraint(['belt_level_id'], ['belt.id'], name='person_belt_level_id_fkey'),
        ForeignKeyConstraint(['role_id'], ['role.id'], name='person_role_id_fkey'),
        PrimaryKeyConstraint('id', name='person_pkey'),
        UniqueConstraint('black_belt_id', name='person_black_belt_id_key'),
        UniqueConstraint('id', name='person_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    first_name: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str] = mapped_column(Text)
    role_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    student_id: Mapped[Optional[str]] = mapped_column(Text)
    belt_level_id: Mapped[Optional[int]] = mapped_column(Integer)
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    dob: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    active: Mapped[Optional[bool]] = mapped_column(Boolean)
    age_category_id: Mapped[Optional[int]] = mapped_column(Integer)
    black_belt_id: Mapped[Optional[str]] = mapped_column(Text, comment='This is the new ID a student gets when progressing to black belt. It can be NULL.')

    age_category: Mapped[Optional['AgeCategory']] = relationship('AgeCategory', back_populates='person')
    belt_level: Mapped[Optional['Belt']] = relationship('Belt', back_populates='person')
    role: Mapped['Role'] = relationship('Role', back_populates='person')
    location: Mapped[List['Location']] = relationship('Location', back_populates='instructor')
    user_person: Mapped[List['UserPerson']] = relationship('UserPerson', back_populates='person')
    class_: Mapped[List['Class']] = relationship('Class', back_populates='instructor')
    promotions: Mapped[List['Promotions']] = relationship('Promotions', back_populates='student')
    attendance: Mapped[List['Attendance']] = relationship('Attendance', back_populates='person')


class Location(Base):
    __tablename__ = 'location'
    __table_args__ = (
        ForeignKeyConstraint(['address_id'], ['address.id'], name='location_address_id_fkey'),
        ForeignKeyConstraint(['instructor_id'], ['person.id'], name='location_instructor_id_fkey'),
        PrimaryKeyConstraint('id', name='location_pkey'),
        UniqueConstraint('id', name='location_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    title: Mapped[str] = mapped_column(String)
    is_dojang: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('now()'))
    instructor_id: Mapped[Optional[int]] = mapped_column(Integer)
    address_id: Mapped[Optional[int]] = mapped_column(Integer)
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    address: Mapped[Optional['Address']] = relationship('Address', back_populates='location')
    instructor: Mapped[Optional['Person']] = relationship('Person', back_populates='location')
    class_: Mapped[List['Class']] = relationship('Class', back_populates='location')
    event: Mapped[List['Event']] = relationship('Event', back_populates='location')
    promotions: Mapped[List['Promotions']] = relationship('Promotions', back_populates='location')


class UserPerson(Base):
    __tablename__ = 'user_person'
    __table_args__ = (
        ForeignKeyConstraint(['person_id'], ['person.id'], name='user_person_person_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='user_person_user_id_fkey'),
        PrimaryKeyConstraint('id', name='user_person_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    person_id: Mapped[int] = mapped_column(Integer)
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    person: Mapped['Person'] = relationship('Person', back_populates='user_person')
    user: Mapped['Users'] = relationship('Users', back_populates='user_person')


class Class(Base):
    __tablename__ = 'class'
    __table_args__ = (
        CheckConstraint('day_number < 7', name='class_day_number_check'),
        ForeignKeyConstraint(['instructor_id'], ['person.id'], name='class_instructor_id_fkey'),
        ForeignKeyConstraint(['location_id'], ['location.id'], name='class_location_id_fkey'),
        PrimaryKeyConstraint('id', name='class_pkey'),
        UniqueConstraint('id', name='class_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    title: Mapped[str] = mapped_column(String)
    day: Mapped[str] = mapped_column(Text)
    start_time: Mapped[datetime.time] = mapped_column(Time)
    end_time: Mapped[datetime.time] = mapped_column(Time)
    location_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('now()'))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    day_number: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(String)
    instructor_id: Mapped[Optional[int]] = mapped_column(Integer)
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    instructor: Mapped[Optional['Person']] = relationship('Person', back_populates='class_')
    location: Mapped['Location'] = relationship('Location', back_populates='class_')
    age_category_XREF: Mapped[List['AgeCategoryXREF']] = relationship('AgeCategoryXREF', back_populates='class_', cascade="all, delete-orphan")
    attendance: Mapped[List['Attendance']] = relationship('Attendance', back_populates='class_')


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = (
        ForeignKeyConstraint(['event_type_id'], ['event_type.id'], name='event_event_type_id_fkey'),
        ForeignKeyConstraint(['location_id'], ['location.id'], name='event_location_id_fkey'),
        PrimaryKeyConstraint('id', name='event_pkey'),
        UniqueConstraint('id', name='event_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    event_type_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[datetime.time] = mapped_column(Time)
    end_time: Mapped[datetime.time] = mapped_column(Time)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    event_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    location_id: Mapped[Optional[int]] = mapped_column(Integer)
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    event_type: Mapped['EventType'] = relationship('EventType', back_populates='event')
    location: Mapped[Optional['Location']] = relationship('Location', back_populates='event')
    age_category_XREF: Mapped[List['AgeCategoryXREF']] = relationship('AgeCategoryXREF', back_populates='event', cascade="all, delete-orphan")


class Promotions(Base):
    __tablename__ = 'promotions'
    __table_args__ = (
        ForeignKeyConstraint(['belt_id'], ['belt.id'], name='promotions_belt_id_fkey'),
        ForeignKeyConstraint(['location_id'], ['location.id'], name='promotions_location_id_fkey'),
        ForeignKeyConstraint(['student_id'], ['person.id'], name='promotions_student_id_fkey'),
        PrimaryKeyConstraint('id', name='promotions_pkey'),
        UniqueConstraint('id', name='promotions_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    promotion_date: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    belt_id: Mapped[int] = mapped_column(Integer)
    student_id: Mapped[int] = mapped_column(Integer)
    location_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    tabs: Mapped[int] = mapped_column(SmallInteger, server_default=text("'0'::smallint"))
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    belt: Mapped['Belt'] = relationship('Belt', back_populates='promotions')
    location: Mapped['Location'] = relationship('Location', back_populates='promotions')
    student: Mapped['Person'] = relationship('Person', back_populates='promotions')


class AgeCategoryXREF(Base):
    __tablename__ = 'age_category_XREF'
    __table_args__ = (
        ForeignKeyConstraint(['age_category_id'], ['age_category.id'], name='age_category_XREF_age_category_id_fkey'),
        ForeignKeyConstraint(['class_id'], ['class.id'], name='age_category_XREF_class_id_fkey'),
        ForeignKeyConstraint(['event_id'], ['event.id'], name='age_category_XREF_event_id_fkey'),
        PrimaryKeyConstraint('id', name='age_category_XREF_pkey'),
        UniqueConstraint('id', name='age_category_XREF_id_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    age_category_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('now()'))
    class_id: Mapped[Optional[int]] = mapped_column(Integer)
    event_id: Mapped[Optional[int]] = mapped_column(Integer)
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    age_category: Mapped['AgeCategory'] = relationship('AgeCategory', back_populates='age_category_XREF')
    class_: Mapped[Optional['Class']] = relationship('Class', back_populates='age_category_XREF')
    event: Mapped[Optional['Event']] = relationship('Event', back_populates='age_category_XREF')


class Attendance(Base):
    __tablename__ = 'attendance'
    __table_args__ = (
        ForeignKeyConstraint(['class_id'], ['class.id'], name='attendance_class_id_fkey'),
        ForeignKeyConstraint(['person_id'], ['person.id'], name='attendance_person_id_fkey'),
        PrimaryKeyConstraint('id', name='attendance_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[datetime.time] = mapped_column(Time)
    person_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('now()'))
    class_id: Mapped[Optional[int]] = mapped_column(Integer)
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    class_: Mapped[Optional['Class']] = relationship('Class', back_populates='attendance')
    person: Mapped['Person'] = relationship('Person', back_populates='attendance')
