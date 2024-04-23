import pm4py
from pm4py import write_xes, read_xes, convert_to_event_log
from pm4py.objects.log.obj import EventLog, Trace, Event
from datetime import datetime
from patterns.singleton import Singleton

class XesWriter(metaclass=Singleton):
    def __init__(self, output_file: str = "output.xes", writing_mode: str = "CREATE", trace_name: str = "trace") -> None:
        self.output_file = output_file
        self.writing_mode = writing_mode
        if writing_mode == "CREATE":
            self.log = EventLog()
        elif writing_mode == "APPEND":
            try:
                df = read_xes(self.output_file)
                self.log = convert_to_event_log(df)
            except Exception:
                self.log = EventLog()
        else:
            raise Exception("Invalid writing mode")
        self.trace = Trace()
        self.trace.attributes["concept:name"] = trace_name
        
    def generate_event(self, concept_type: str, concept_name: str, lineno: int, timestamp: datetime = None) -> None:
        event = Event()
        event["concept:name"] = f"{concept_type}: {concept_name} lineno: {lineno}"
        if timestamp is not None:
            event["time:timestamp"] = timestamp
        self.trace.append(event)
    
    def write(self) -> None:
        self.log.append(self.trace)
        write_xes(self.log, self.output_file)
        