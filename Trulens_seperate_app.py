## ref link
##https://github.com/truera/trulens/blob/main/trulens_eval/examples/experimental/virtual_example.ipynb

from trulens_eval import Tru
import os
os.environ["OPENAI_API_KEY"] = "sk-*"
tru = Tru()
tru.reset_database() # if needed

tru.run_dashboard()

# VirtualApp setup. You can store any information you would like by passing in a
# VirtualApp or a plain dictionary to TruVirtual (later). This may involve an
# index of components or versions, or anything else. You can refer to these
# values for evaluating feedback.

virtual_app = dict(
    llm=dict(
        modelname="some llm component model name"
    ),
    template="information about the template I used in my app",
    debug="all of these fields are completely optional"
)

# (Optional) If you use the `VirtualApp` class instead of a plain dictionary,
# you can use selectors to position the virtual app components and their
# properties.

from trulens_eval.schema import Select
from trulens_eval.tru_virtual import VirtualApp

virtual_app = VirtualApp(virtual_app) # can start with the prior dictionary
virtual_app[Select.RecordCalls.llm.maxtokens] = 1024

# Using Selectors here lets you use reuse the setup you use to define feedback
# functions (later in the notebook). We will use `retriever_component`
# exemplified below place information about retrieved context in a virtual
# record that will match the information about the retriever component in the
# virtual app. While this is not necessary, laying out the virtual app and
# virtual records in a mirrored fashion as would be the same for real apps may
# aid interpretability.

retriever_component = Select.RecordCalls.retriever
virtual_app[retriever_component] = "this is the retriever component"


virtual_app

# Data. To add data to the database, you can either create the `Record`, or use
# `VirtualRecord` class which helps you construct records for virtual models.
# The arguments to VirtualRecord are the same as for Record except that calls
# are specified using selectors. In the below example, we add two records with
# both containing the inputs and outputs to some context retrieval component.
# You do not need to provide information that you do not wish to track or
# evaluate on. The selectors refer to methods which can be selected for in
# feedback which we show below.

from trulens_eval.tru_virtual import VirtualRecord

# The selector for a presumed context retrieval component's call to
# `get_context`. The names are arbitrary but may be useful for readability on
# your end.
context_call = retriever_component.get_context

rec1 = VirtualRecord(
    main_input="Where is Germany?",
    main_output="Germany is in Europe",
    calls=
        {
            context_call: dict(
                args=["Where is Germany?"],
                rets=["Germany is a country located in Europe."]
            )
        }
    )
rec2 = VirtualRecord(
    main_input="Where is Germany?",
    main_output="Poland is in Europe",
    calls=
        {
            context_call: dict(
                args=["Where is Germany?"],
                rets=["Poland is a country located in Europe."]
            )
        }
    )

data = [rec1, rec2]

# Run to read more about VirtualRecord:
# help(VirtualRecord)

# The same feedback function as the langchain quickstart except the selector for
# context is different.

from trulens_eval.feedback.provider import OpenAI
from trulens_eval.feedback.feedback import Feedback
from trulens_eval.schema import FeedbackResult

# Initialize provider class
openai = OpenAI()

# Select context to be used in feedback. We select the return values of the
# virtual `get_context` call in the virtual `retriever` component. Names are
# arbitrary except for `rets`.
context = context_call.rets[:]

from trulens_eval.feedback import Groundedness
grounded = Groundedness(groundedness_provider=OpenAI())
# Define a groundedness feedback function
f_groundedness = (
    Feedback(grounded.groundedness_measure_with_cot_reasons)
    .on(context.collect()) # collect context chunks into a list
    .on_output()
    .aggregate(grounded.grounded_statements_aggregator)
)

# Question/answer relevance between overall question and answer.
f_qa_relevance = Feedback(openai.relevance).on_input_output()

# Question/statement relevance between question and each context chunk.
f_context_relevance = (
    Feedback(openai.qs_relevance)
    .on_input()
    .on(context)
)

from trulens_eval.tru_virtual import TruVirtual

virtual_recorder = TruVirtual(
    app_id="a virtual app",
    app=virtual_app,
    feedbacks=[ f_qa_relevance]
)

# Run to read more about TruVirtual:
# help(TruVirtual)

from trulens_eval.schema import FeedbackMode

for rec in data:
    virtual_recorder.add_record(rec)

    # Can wait for feedback on `add_record`:
    # virtual_recorder.add_record(rec, feedback_mode=FeedbackMode.WITH_APP)

# Run to read more about add_record:
help(virtual_recorder.add_record)

# Retrieve feedback results. You can either browse the dashboard or retrieve the
# results from the record after it has been `add_record`ed.

for rec in data:
    print(rec.main_input, "-->", rec.main_output)

    for feedback, feedback_result in rec.wait_for_feedback_results().items():
        print("\t", feedback.name, feedback_result.result)
        
    print()