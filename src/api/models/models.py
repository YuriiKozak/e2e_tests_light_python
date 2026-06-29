from datetime import date
from enum import Enum, StrEnum
from typing import Any

from pydantic import AwareDatetime, BaseModel, EmailStr, Field


class PaginationMeta(BaseModel):
    total: int | None = None
    page: int | None = None
    per_page: int | None = None


class ErrorResponse(BaseModel):
    error: str


class AnalyticsTestsResponse(BaseModel):
    data: list[dict[str, Any]] | None = Field(
        None,
        description="Rows of tests matching the kind. Row shape varies per kind.\nCommon fields: `test_uid`, `title`, `suite_uid`, `suite_title`, `priority`, `executed_at`.\n`flaky` adds `flaky_rate`, `runStatuses`.\n`slow` adds `run_time`, `threshold`, `testrun_id`, `run_uid`, `run_title`, `status`.\n`failures` groups by error message.\n`issues` / `defects` group by linked JIRA issue.\n",
    )
    meta: PaginationMeta | None = None
    config: dict[str, Any] | None = Field(
        None,
        description="Query configuration in effect (e.g. `min`/`max` for flaky, `threshold` for slow).",
    )
    filter_values: dict[str, Any] | None = None


class Meta(BaseModel):
    kind: str | None = None
    primary_key: str | None = None
    primary_label: str | None = None
    data_keys: list[str] | None = None
    is_empty: bool | None = None


class AnalyticsStatsResponse(BaseModel):
    data: list[dict[str, Any]] | None = Field(
        None,
        description="Aggregated rows. Shape depends on the stats kind (see `meta.data_keys`).\n`project-summary` and `runs-summary` return one row per project/run with 20+ fields.\n`*-by-date` kinds return one row per day keyed by `date`.\n",
    )
    meta: Meta | None = None
    filter_values: dict[str, Any] | None = None


class Label(BaseModel):
    title: str | None = None
    slug: str | None = None


class CiProfile(BaseModel):
    profile_name: str | None = None
    service: str | None = None
    config: dict[str, Any] | None = None
    pass_testomatio_key: bool | None = None
    pass_testomatio_url: bool | None = None
    pass_run_id: bool | None = None


class ProjectInfo(BaseModel):
    title: str | None = None
    project_id: str | None = Field(None, description="Project slug identifier")
    framework: str | None = None
    language: str | None = None
    status: str | None = None
    repository_url: str | None = None
    artifacts_storage_enabled: bool | None = Field(
        None,
        description="True when all required artifact storage credentials are configured",
    )
    environments: list[str] | None = None
    labels: list[Label] | None = None
    tags: list[str] | None = None
    subscription: str | None = Field(
        None,
        description='Active subscription plan title (e.g. "Enterprise"). Null when no subscription is active.',
    )
    features: list[str] | None = Field(
        None,
        description='Feature keys enabled by the active subscription (e.g. "milestones", "analytics", "branches").',
    )
    ci_profiles: list[CiProfile] | None = None


class Type(StrEnum):
    test = "test"


class Priority(Enum):
    low = "low"
    normal = "normal"
    important = "important"
    high = "high"
    critical = "critical"
    none_type_none = None


class Type1(StrEnum):
    suite = "suite"


class SourceType(StrEnum):
    jira = "jira"
    confluence = "confluence"
    file = "file"
    text = "text"


class LinkedRequirement(BaseModel):
    id: str | None = Field(None, description="ID (8-char)")
    title: str | None = None
    source_type: SourceType | None = None
    global_: bool | None = Field(
        None,
        alias="global",
        description="True if this is a global (project-level) requirement",
    )


class Type2(StrEnum):
    requirement = "requirement"


class Status(StrEnum):
    pending = "pending"
    processed = "processed"
    failed = "failed"
    outdated = "outdated"


class Level(StrEnum):
    project = "project"
    suite = "suite"
    none = "none"


class Requirement(BaseModel):
    id: str | None = Field(None, description="Public ID (8-char)")
    type: Type2 | None = None
    title: str | None = None
    description: str | None = None
    summary: str | None = None
    details: str | None = Field(
        None, description="Extended details or raw content of the requirement"
    )
    message: str | None = Field(None, description="Processing message or error details")
    source_type: SourceType | None = None
    source_key: str | None = None
    status: Status | None = None
    active: bool | None = None
    global_: bool | None = Field(None, alias="global")
    level: Level | None = Field(None, description="Scope level of the requirement")
    url: str | None = Field(
        None,
        description="URL to this requirement in Testomat.io (returned on create/update)",
    )


class RequirementCreateInput(BaseModel):
    title: str
    source_type: SourceType
    description: str | None = Field(
        None,
        description="Required for text requirements. Must be at least 500 characters.",
    )
    details: str | None = None
    active: bool | None = None
    global_: bool | None = Field(None, alias="global")
    confluence_url: str | None = Field(
        None, description="Required for confluence requirements"
    )
    files: list[bytes] | None = Field(
        None,
        description="Files to attach to the requirement. Allowed extensions: pdf, doc, docx, xls, xlsx, csv, txt, md, html, xml, json, feature, png, jpg, jpeg, gif, svg, webp",
    )


class RequirementUpdateInput(BaseModel):
    title: str | None = None
    description: str | None = Field(
        None, description="Only applied for text requirements"
    )
    details: str | None = None
    active: bool | None = None
    global_: bool | None = Field(None, alias="global")
    files: list[bytes] | None = Field(
        None,
        description="Files to attach to the requirement. Allowed extensions: pdf, doc, docx, xls, xlsx, csv, txt, md, html, xml, json, feature, png, jpg, jpeg, gif, svg, webp",
    )


class Type3(StrEnum):
    plan = "plan"


class Kind(StrEnum):
    manual = "manual"
    automated = "automated"
    mixed = "mixed"


class Type4(StrEnum):
    run = "run"


class AssignStrategy(StrEnum):
    test = "test"
    random = "random"
    none = "none"


class Type5(StrEnum):
    testrun = "testrun"


class Testrun(BaseModel):
    id: int | None = None
    type: Type5 | None = None
    test_title: str | None = None
    suite_title: str | None = Field(
        None, description="Tag-stripped title of the test's parent suite"
    )
    message: str | None = None
    status: str | None = Field(
        None, description="One of: passed, failed, skipped, pending"
    )
    substatus: str | None = None
    run_time: int | None = Field(
        None, description="Test execution duration in milliseconds"
    )
    automated: bool | None = None
    assigned_to: EmailStr | None = None
    run_id: str | None = Field(None, description="Public UID of the parent run")
    test_id: str | None = Field(None, description="Public UID of the associated test")
    test_version: int | None = Field(
        None,
        description="Version index of the test at the time this testrun was executed. Returned only on show for non-pending testruns.",
    )
    description: str | None = Field(
        None,
        description="Description of the test at the version captured for this testrun. Returned only on show for non-pending testruns.",
    )
    url: str | None = Field(
        None,
        description="URL to this testrun in Testomat.io (returned on create/update)",
    )


class Type6(StrEnum):
    rungroup = "rungroup"


class Rungroup(BaseModel):
    id: str | None = Field(None, description="Public UID")
    type: Type6 | None = None
    title: str | None = None
    clean_title: str | None = None
    emoji: str | None = None
    description: str | None = None
    kind: str | None = None
    status: str | None = None
    pin: bool | None = None
    runs_count: int | None = None
    finished_at: AwareDatetime | None = None
    tests_count: int | None = None
    archived_at: AwareDatetime | None = None
    updated_at: AwareDatetime | None = None
    parent_id: str | None = Field(
        None, description="Public UID of the parent run group"
    )
    children: list[Rungroup] | None = Field(
        None,
        description="Nested child run groups (present in tree responses when children exist)",
    )
    url: str | None = Field(
        None,
        description="URL to this run group in Testomat.io (returned on create/update)",
    )


class Type7(StrEnum):
    step = "step"


class Label1(BaseModel):
    id: str | None = Field(None, description="Label slug")
    title: str | None = None
    color: str | None = None
    position: int | None = None
    visibility: str | None = None
    list: bool | None = None


class TagSummary(BaseModel):
    title: str | None = None
    count: int | None = None


class Type8(StrEnum):
    issue = "issue"
    jira_issue = "jira_issue"


class Issue(BaseModel):
    id: int | None = Field(None, description="Database ID")
    type: Type8 | None = None
    title: str | None = None
    url: str | None = None
    source: str | None = Field(
        None, description="Integration source (e.g. github, jira, linear, link)"
    )
    resource_type: str | None = Field(
        None, description="Type of linked resource (test, suite, run, testrun, plan)"
    )
    resource_id: str | None = Field(
        None, description="Public UID of the linked resource"
    )
    jira_id: str | None = Field(
        None, description="Jira issue key (only for type=jira_issue)"
    )
    synced: bool | None = Field(
        None, description="Jira sync status (only for type=jira_issue)"
    )


class LabelAttachment(BaseModel):
    id: str | None = Field(None, description="Label slug")
    title: str | None = None
    color: str | None = None
    position: int | None = None
    visibility: str | None = None
    list: bool | None = None
    value: str | None = Field(
        None, description="Custom field value (if label has a field type)"
    )
    short: str | None = Field(None, description="Short display format for the field")


class Action(StrEnum):
    add = "add"
    remove = "remove"


class Type9(StrEnum):
    label = "label"
    custom_field = "custom_field"
    tag = "tag"
    milestone = "milestone"
    issue = "issue"
    jira = "jira"
    requirement = "requirement"
    public_report = "public_report"


class Value(BaseModel):
    passcode: bool | None = Field(
        None,
        description="Set to true to protect the public report with a randomly generated passcode.",
    )
    expires_at: date | None = Field(
        None,
        description='Expiration date for the public report link (e.g. "2026-12-31"). Must be at least 1 day from now. Defaults to 1 week from today if not provided.',
    )


class LinkAction(BaseModel):
    action: Action
    type: Type9
    value: str | Value | None = None


class Type10(StrEnum):
    milestone = "milestone"


class Status1(StrEnum):
    created = "created"
    active = "active"
    closed = "closed"


class Milestone(BaseModel):
    id: str | None = Field(None, description="Milestone slug")
    type: Type10 | None = None
    title: str | None = None
    value: str | None = None
    display_title: str | None = None
    status: Status1 | None = None
    description: str | None = None
    goal: str | None = None
    start_date: date | None = None
    release_date: date | None = None
    url: str | None = None
    expired: bool | None = None
    project_scoped: bool | None = None


class IssueInput(BaseModel):
    url: str | None = Field(
        None,
        description="Issue URL (for generic issues). Provide either url or jira_id.",
    )
    jira_id: str | None = Field(
        None,
        description="Jira issue key (e.g. TST-123). Provide either url or jira_id.",
    )


class Priority1(StrEnum):
    low = "low"
    normal = "normal"
    important = "important"
    high = "high"
    critical = "critical"


class TestInput(BaseModel):
    title: str
    description: str | None = None
    emoji: str | None = None
    suite_id: str = Field(..., description="Public UID of the parent suite")
    priority: Priority1 | None = None
    assigned_to: EmailStr | None = Field(
        None, description="Email address of a non-readonly project member to assign."
    )
    code: str | None = None
    state: str | None = None
    link: list[LinkAction] | None = Field(
        None, description="Add/remove labels, tags, issues, or jira links"
    )


class SuiteChildInput(BaseModel):
    title: str
    description: str | None = None
    emoji: str | None = None
    children: list[SuiteChildInput] | None = Field(
        None, description="Nested child suites (recursive)"
    )


class PlanInput(BaseModel):
    title: str
    description: str | None = None
    kind: str | None = None
    hidden: bool | None = None
    as_manual: bool | None = None
    test_ids: list[str] | None = Field(
        None,
        description="List of test IDs (8-char) to include in the plan. If omitted, all tests matching the plan kind are included.",
    )
    suite_ids: list[str] | None = Field(
        None,
        description="List of suite IDs (8-char) to include in the plan. If omitted, all suites are considered.",
    )
    tql: str | None = Field(
        None,
        description="TQL query expression to filter tests for the plan (e.g. `priority == 'high'`).",
        examples=["priority == 'high'"],
    )
    link: list[LinkAction] | None = Field(
        None, description="Add/remove labels or issues/jira links"
    )


class RunCreateInput(BaseModel):
    title: str
    description: str | None = None
    plan_ids: list[str] | None = Field(
        None, description="List of plan public UIDs to include in the run"
    )
    kind: Kind | None = None
    rungroup_id: str | None = Field(None, description="Public UID of the run group")
    env: str | None = Field(
        None, description="Environment(s) for this run, comma-separated"
    )
    assigned_to: EmailStr | None = Field(
        None, description="Email address of a non-readonly project member to assign."
    )
    assign_strategy: AssignStrategy | None = Field(
        None,
        description="Strategy for assigning testruns to users:\n- `test`: assign each testrun to the user assigned to the corresponding test\n- `random`: distribute testruns evenly across all run assistants\n- `none`: no automatic assignment (default)\n",
    )
    test_ids: list[str] | None = Field(
        None,
        description='List of test public UIDs to include in the run. Pass ["*"] to include all tests in the project.',
    )
    suite_ids: list[str] | None = Field(
        None,
        description="List of suite public UIDs whose tests will be included in the run",
    )
    envs: list[str] | None = Field(
        None,
        description="List of environments for multi-environment run creation. Only applicable when `kind` is `manual` (or not specified). When provided, a separate Run is created for each environment and grouped into a Rungroup. Ignored for `automated` and `mixed` kinds.\n",
        examples=[["staging", "production"]],
    )
    link: list[LinkAction] | None = Field(
        None, description="Add/remove labels or issues/jira links"
    )


class StatusEvent(StrEnum):
    finish = "finish"
    finish_manual = "finish_manual"
    launch = "launch"
    rerun = "rerun"
    scheduled = "scheduled"
    terminate = "terminate"


class RunUpdateInput(BaseModel):
    title: str | None = None
    description: str | None = None
    kind: Kind | None = None
    rungroup_id: str | None = Field(None, description="Public UID of the run group")
    env: str | None = Field(
        None, description="Environment(s) for this run, comma-separated"
    )
    status_event: StatusEvent | None = Field(
        None,
        description="Trigger a run status transition:\n- `finish`: Finish an automated run; final status is calculated from test results\n- `finish_manual`: Finish a manual/mixed run; final status is calculated from test results\n- `launch`: Start the run\n- `rerun`: Restart the run\n- `scheduled`: Move the run back to scheduled state\n- `terminate`: Stop the run and mark it as terminated\n",
    )
    assigned_to: EmailStr | None = Field(
        None, description="Email address of a non-readonly project member to assign."
    )
    assign_strategy: AssignStrategy | None = Field(
        None,
        description="Strategy for assigning testruns to users:\n- `test`: assign each testrun to the user assigned to the corresponding test\n- `random`: distribute testruns evenly across all run assistants\n- `none`: no automatic assignment (default)\n",
    )
    test_ids: list[str] | None = Field(
        None, description="List of test public UIDs to append to the run configuration"
    )
    suite_ids: list[str] | None = Field(
        None,
        description="List of suite public UIDs whose tests will be appended to the run configuration",
    )
    link: list[LinkAction] | None = Field(
        None, description="Add/remove labels or issues/jira links"
    )


class TestrunInput(BaseModel):
    run_id: str = Field(..., description="Public UID of the run")
    test_id: str | None = Field(None, description="Public UID of the test")
    status: str | None = Field(
        None, description="One of: passed, failed, skipped, pending"
    )
    message: str | None = None
    run_time: float | None = None
    assigned_to: EmailStr | None = Field(
        None, description="Email address of a non-readonly project member to assign."
    )
    test_title: str | None = None
    automated: bool | None = None


class RungroupChildInput(BaseModel):
    title: str
    description: str | None = None
    emoji: str | None = None
    kind: str | None = None
    pin: bool | None = None
    status: str | None = None
    children: list[RungroupChildInput] | None = Field(
        None, description="Nested child run groups (recursive)"
    )


class StepInput(BaseModel):
    title: str
    description: str | None = None
    link: list[LinkAction] | None = Field(None, description="Add/remove labels")


class SnippetInput(BaseModel):
    title: str
    description: str | None = None
    link: list[LinkAction] | None = Field(None, description="Add/remove labels")


class VisibilityEnum(StrEnum):
    filter = "filter"
    list = "list"


class ScopeEnum(StrEnum):
    tests = "tests"
    suites = "suites"
    runs = "runs"
    plans = "plans"
    steps = "steps"
    templates = "templates"


class LabelInput(BaseModel):
    title: str
    color: str | None = None
    visibility: list[VisibilityEnum] | None = Field(
        None,
        description="Where the label appears: 'filter' — in filter panel, 'list' — on entity list page",
    )
    scope: list[ScopeEnum] | None = None
    field: dict[str, Any] | None = None


class Test(BaseModel):
    id: str | None = Field(None, description='Public UID (e.g. "@Txxxxx")')
    type: Type | None = None
    title: str | None = None
    emoji: str | None = None
    state: str | None = None
    is_shared: bool | None = None
    assigned_to: EmailStr | None = None
    priority: Priority | None = None
    public_title: str | None = None
    clean_title: str | None = None
    self_tags: list[str] | None = None
    sync: bool | None = None
    code: str | None = None
    description: str | None = None
    position: int | None = None
    suite_id: str | None = Field(None, description="Public UID of the parent suite")
    suite_title: str | None = Field(
        None, description="Tag-stripped title of the parent suite"
    )
    labels: list[LabelAttachment] | None = None
    url: str | None = Field(
        None, description="URL to this test in Testomat.io (returned on create/update)"
    )


class Suite(BaseModel):
    id: str | None = Field(None, description="Public UID")
    type: Type1 | None = None
    title: str | None = None
    emoji: str | None = None
    public_title: str | None = None
    is_shared: bool | None = None
    file_type: str | None = Field(
        None,
        description="Auto-detected: 'folder' if suite has children, 'file' otherwise",
    )
    test_count: int | None = None
    assigned_to: EmailStr | None = None
    clean_title: str | None = None
    tags: list[str] | None = None
    sync: bool | None = None
    description: str | None = None
    file: str | None = Field(None, description="File path associated with this suite")
    parent_id: str | None = Field(
        None, description="Public UID of the parent suite, or null for root suites"
    )
    labels: list[LabelAttachment] | None = None
    requirements: list[LinkedRequirement] | None = Field(
        None, description="Attached and global requirements for this suite"
    )
    children: list[Suite] | None = Field(
        None,
        description="Nested child suites (present in tree responses when children exist)",
    )
    url: str | None = Field(
        None, description="URL to this suite in Testomat.io (returned on create/update)"
    )


class Plan(BaseModel):
    id: str | None = Field(None, description="Public UID")
    type: Type3 | None = None
    title: str | None = None
    description: str | None = None
    kind: Kind | None = Field(None, description="Plan type")
    hidden: bool | None = None
    labels: list[LabelAttachment] | None = None
    url: str | None = Field(
        None, description="URL to this plan in Testomat.io (returned on create/update)"
    )


class Run(BaseModel):
    id: str | None = Field(None, description="Public UID")
    type: Type4 | None = None
    title: str | None = None
    clean_title: str | None = None
    kind: Kind | None = Field(None, description="Run type")
    rungroup_id: str | None = Field(
        None, description="Public UID of the rungroup this run belongs to"
    )
    plan_id: str | None = Field(
        None, description="Public UID of the plan this run created from"
    )
    assigned_to: EmailStr | None = None
    assign_strategy: AssignStrategy | None = None
    env: str | None = Field(
        None, description="Environment(s) for this run, comma-separated"
    )
    description: str | None = None
    labels: list[LabelAttachment] | None = None
    public_report_url: str | None = Field(
        None,
        description="Public shareable URL of the run report. Present only when the run is published.",
    )
    public_report_passcode: int | None = Field(
        None,
        description="Numeric passcode protecting the public report. Present only when the run is published.",
    )
    public_report_expires_at: AwareDatetime | None = Field(
        None,
        description="Expiration date of the public report link. Present only when the run is published.",
    )
    url: str | None = Field(
        None, description="URL to this run in Testomat.io (returned on create/update)"
    )


class Step(BaseModel):
    id: int | None = None
    type: Type7 | None = None
    title: str | None = None
    description: str | None = None
    is_snippet: bool | None = None
    kind: str | None = None
    usage_count: int | None = None
    keywords: list[str] | None = None
    labels: list[LabelAttachment] | None = None
    url: str | None = Field(
        None, description="URL to this step in Testomat.io (returned on create/update)"
    )


class SuiteInput(BaseModel):
    title: str
    description: str | None = None
    emoji: str | None = None
    parent_id: str | None = Field(None, description="Public UID of the parent suite")
    file_type: str | None = Field(
        None,
        description="Auto-detected from children: 'folder' if children provided, 'file' otherwise. Can be overridden explicitly.",
    )
    assigned_to: EmailStr | None = Field(
        None, description="Email address of a non-readonly project member to assign."
    )
    file: str | None = Field(
        None,
        description="File path to associate with the suite. Only applicable when file_type is 'file'.",
    )
    children: list[SuiteChildInput] | None = Field(
        None,
        description="Nested child suites to create recursively. When provided, file_type is auto-set to 'folder'.",
    )
    link: list[LinkAction] | None = Field(
        None, description="Add/remove labels, tags, issues, or jira links"
    )


class RungroupInput(BaseModel):
    title: str
    description: str | None = None
    emoji: str | None = None
    kind: str | None = None
    pin: bool | None = None
    status: str | None = None
    parent_id: str | None = Field(
        None, description="Public UID of the parent run group"
    )
    children: list[RungroupChildInput] | None = Field(
        None, description="Nested child run groups to create recursively"
    )


Rungroup.model_rebuild()
SuiteChildInput.model_rebuild()
RungroupChildInput.model_rebuild()
Suite.model_rebuild()
