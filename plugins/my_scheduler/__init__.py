import pybossa.sched as sched
from pybossa.forms.forms import TaskSchedulerForm
from flask.ext.plugins import Plugin
from functools import wraps
from pybossa.core import project_repo
from pybossa.model.user import User
from flask.ext.login import current_user
from flask import session
from sqlalchemy.sql import func, desc
from sqlalchemy import and_
from pybossa.model import DomainObject
from pybossa.model.task import Task
from pybossa.model.task_run import TaskRun
from pybossa.model.counter import Counter
from pybossa.core import db
import random
from pybossa.plugins.quiz import models

__plugin__ = "FRGScheduler"
__version__ = "0.0.1"

SCHEDULER_NAME = 'FRG'
SCHEDULER_DISPLAY_NAME = "FRG"
session = db.slave_session

def get_task(#project_id, user_id=None, user_ip=None, n_answers=30, offset=0):
	project_id, user_id=None, user_ip=None,
	                         external_uid=None, offset=0, limit=1,
	                         orderby='priority_0', desc=True):
	project = project_repo.get(project_id)
	"""Get all available tasks for a given project and user."""
	data = None
	if user_id and not user_ip and not external_uid:
		subquery = session.query(TaskRun.task_id).filter_by(project_id=project_id, user_id=user_id)
	else:
		 if not user_ip:
		 	 user_ip = '127.0.0.1'
		 if user_ip and not external_uid:
		 	subquery = session.query(TaskRun.task_id).filter_by(project_id=project_id, user_ip=user_ip)
		 else:
		 	subquery = session.query(TaskRun.task_id).filter_by(project_id=project_id, external_uid=external_uid)

	query = session.query(Task).filter(and_(~Task.id.in_(subquery.subquery()),
                                            Task.project_id == project_id,Task.state != 'completed'))
	dictobj={"images":[],"videos":[],"documents":[],"audios":[]}

	for q in query:
		if q.info["type"]=="images":
			#dictobj.update({"images":q})
			dictobj["images"].append(q)
		elif q.info["type"]=="documents":
			#dictobj.update({"documents":q})
			dictobj["documents"].append(q)
		elif q.info["type"]=="videos":
			#dictobj.update({"videos":q})
			dictobj["videos"].append(q)
		elif q.info["type"]=="audios":
			#dictobj.update({"audios":q})
			dictobj["audios"].append(q)
	if project and len(project.tasks)>0:
		score=models.user_score.query.filter_by(user_id=current_user.id, project_id=project_id).first()
		image_score=score.image_score
		video_score=score.video_score
		audio_score=score.audio_score
		document_score=score.document_score
		dict_score={"images":image_score,"videos":video_score,"audios":audio_score,"documents":document_score}
		for key, value in dictobj.iteritems():
			if(len(dictobj[key])==0):
				dict_score.pop(key, None)
		sort_dict=sorted(dict_score.items(),key = lambda t:t[1])
		print "Broken Pipe \n\n"
		print dictobj['images']
		top_score=[]
		if(len(sort_dict)==1):
			top_score=[dictobj[sort_dict[0][0]]]
		else :
			top_score=[dictobj[sort_dict[len(sort_dict)-1][0]],dictobj[sort_dict[len(sort_dict)-2][0]]]
		return top_score
	else:
		return None
    #pass


def with_frg_scheduler(f):
    @wraps(f)
    def wrapper(project_id, sched, user_id=None, user_ip=None, offset=0):
        if sched == SCHEDULER_NAME:
            return get_task(project_id, user_id, user_ip, offset=offset)
        return f(project_id, sched, user_id=user_id, user_ip=user_ip, offset=offset)
    return wrapper


def variants_with_frg_scheduler(f):
    @wraps(f)
    def wrapper():
        return f() + [(SCHEDULER_NAME, SCHEDULER_DISPLAY_NAME)]
    return wrapper


class FRGScheduler(Plugin):

    def setup(self):
        sched.new_task = with_frg_scheduler(sched.new_task)
        sched.sched_variants = variants_with_frg_scheduler(sched.sched_variants)
TaskSchedulerForm.update_sched_options(sched.sched_variants())
