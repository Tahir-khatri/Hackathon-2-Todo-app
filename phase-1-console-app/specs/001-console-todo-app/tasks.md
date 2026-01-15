# Tasks: In-Memory Python Console Todo App (Phase I)

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Unit tests included per constitution requirement (VI. Testing Discipline).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Status**: ✅ COMPLETE - All 47 tasks completed, 50 tests passing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure) ✅ COMPLETE

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure per plan.md (src/, src/models/, src/services/, src/cli/, tests/, tests/unit/, tests/integration/)
- [x] T002 Initialize Python project with pyproject.toml for Python 3.13+
- [x] T003 [P] Create package marker files (__init__.py) in all directories
- [x] T004 [P] Configure pytest in pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites) ✅ COMPLETE

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create TaskStatus enum in src/models/task.py
- [x] T006 Create Task dataclass in src/models/task.py (id, description, status, created_at attributes)
- [x] T007 Create TaskService class skeleton in src/services/task_service.py with storage dict and next_id counter
- [x] T008 [P] Create CLI input utilities in src/cli/handlers.py (get_user_input with KeyboardInterrupt handling)
- [x] T009 [P] Create menu display function in src/cli/menu.py (display_menu showing all 6 options)
- [x] T010 Create main application entry point in src/main.py with main loop structure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add a New Task (Priority: P1) 🎯 MVP ✅ COMPLETE

**Goal**: Users can add new tasks with descriptions to track work

**Independent Test**: Launch app, select "Add Task", enter description, verify task appears with unique ID and "Pending" status

### Tests for User Story 1

- [x] T011 [P] [US1] Unit test for TaskService.add_task() in tests/unit/test_task_service.py
- [x] T012 [P] [US1] Unit test for Task model creation in tests/unit/test_task_model.py

### Implementation for User Story 1

- [x] T013 [US1] Implement add_task method in src/services/task_service.py (assign ID, set PENDING status, store task)
- [x] T014 [US1] Implement description validation in src/services/task_service.py (1-500 chars, non-empty)
- [x] T015 [US1] Implement handle_add_task handler in src/cli/handlers.py (prompt for description, call service, display confirmation)
- [x] T016 [US1] Wire Add Task menu option (1) to handler in src/main.py

**Checkpoint**: Users can add tasks - US1 independently testable

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1) 🎯 MVP ✅ COMPLETE

**Goal**: Users can view all tasks with ID, description, and status

**Independent Test**: Add several tasks, select "View All Tasks", verify formatted list shows all tasks with [ ] and [x] indicators

### Tests for User Story 2

- [x] T017 [P] [US2] Unit test for TaskService.get_all_tasks() in tests/unit/test_task_service.py
- [x] T018 [P] [US2] Unit test for TaskService.get_task_count() in tests/unit/test_task_service.py

### Implementation for User Story 2

- [x] T019 [US2] Implement get_all_tasks method in src/services/task_service.py (return list of all tasks)
- [x] T020 [US2] Implement get_task_count method in src/services/task_service.py
- [x] T021 [US2] Implement handle_view_tasks handler in src/cli/handlers.py (display formatted list or empty message)
- [x] T022 [US2] Wire View All Tasks menu option (2) to handler in src/main.py

**Checkpoint**: Users can add and view tasks - US1+US2 form core MVP

---

## Phase 5: User Story 3 - Mark Task as Complete (Priority: P2) ✅ COMPLETE

**Goal**: Users can mark tasks as complete to track progress

**Independent Test**: Add a task, mark it complete by ID, verify status changes to "Completed"

### Tests for User Story 3

- [x] T023 [P] [US3] Unit test for TaskService.mark_complete() in tests/unit/test_task_service.py
- [x] T024 [P] [US3] Unit test for TaskService.get_task() in tests/unit/test_task_service.py

### Implementation for User Story 3

- [x] T025 [US3] Implement get_task method in src/services/task_service.py (lookup by ID, return None if not found)
- [x] T026 [US3] Implement mark_complete method in src/services/task_service.py (change status to COMPLETED)
- [x] T027 [US3] Implement get_task_id helper in src/cli/handlers.py (validate numeric input, positive integer)
- [x] T028 [US3] Implement handle_mark_complete handler in src/cli/handlers.py (prompt for ID, call service, display result)
- [x] T029 [US3] Wire Mark Complete menu option (3) to handler in src/main.py

**Checkpoint**: Users can add, view, and complete tasks

---

## Phase 6: User Story 4 - Update a Task (Priority: P3) ✅ COMPLETE

**Goal**: Users can update task descriptions to correct or add detail

**Independent Test**: Add a task, update its description, verify change persists in view

### Tests for User Story 4

- [x] T030 [P] [US4] Unit test for TaskService.update_task() in tests/unit/test_task_service.py

### Implementation for User Story 4

- [x] T031 [US4] Implement update_task method in src/services/task_service.py (find by ID, update description)
- [x] T032 [US4] Implement handle_update_task handler in src/cli/handlers.py (prompt for ID and new description, call service)
- [x] T033 [US4] Wire Update Task menu option (4) to handler in src/main.py

**Checkpoint**: CRUD operations complete except Delete

---

## Phase 7: User Story 5 - Delete a Task (Priority: P3) ✅ COMPLETE

**Goal**: Users can delete tasks to remove items no longer needed

**Independent Test**: Add a task, delete by ID, verify it no longer appears in list

### Tests for User Story 5

- [x] T034 [P] [US5] Unit test for TaskService.delete_task() in tests/unit/test_task_service.py

### Implementation for User Story 5

- [x] T035 [US5] Implement delete_task method in src/services/task_service.py (remove from storage, return success)
- [x] T036 [US5] Implement handle_delete_task handler in src/cli/handlers.py (prompt for ID, call service, display result)
- [x] T037 [US5] Wire Delete Task menu option (5) to handler in src/main.py

**Checkpoint**: Full CRUD operations available

---

## Phase 8: User Story 6 - Exit the Application (Priority: P3) ✅ COMPLETE

**Goal**: Users can exit gracefully with data loss warning

**Independent Test**: Select "Exit", verify goodbye message displays and app terminates

### Implementation for User Story 6

- [x] T038 [US6] Implement handle_exit handler in src/cli/handlers.py (display data loss warning, goodbye message, raise SystemExit)
- [x] T039 [US6] Wire Exit menu option (6) to handler in src/main.py
- [x] T040 [US6] Ensure Ctrl+C handling displays goodbye message in src/main.py

**Checkpoint**: Application complete with graceful exit

---

## Phase 9: Polish & Cross-Cutting Concerns ✅ COMPLETE

**Purpose**: Improvements that affect multiple user stories

- [x] T041 Add comprehensive error messages for all invalid input scenarios in src/cli/handlers.py
- [x] T042 [P] Add docstrings to all public methods in src/models/task.py
- [x] T043 [P] Add docstrings to all public methods in src/services/task_service.py
- [x] T044 [P] Add docstrings to all public functions in src/cli/handlers.py
- [x] T045 [P] Integration test for full CLI flow in tests/integration/test_cli_flow.py
- [x] T046 Create README.md with setup and usage instructions
- [x] T047 Run all tests and verify 100% pass rate

---

## Final Status

### Test Results
- **Unit Tests**: 39 passed
- **Integration Tests**: 11 passed
- **Total**: 50 passed, 0 failed

### Files Created
- `src/__init__.py`
- `src/main.py`
- `src/models/__init__.py`
- `src/models/task.py`
- `src/services/__init__.py`
- `src/services/task_service.py`
- `src/cli/__init__.py`
- `src/cli/menu.py`
- `src/cli/handlers.py`
- `tests/__init__.py`
- `tests/unit/__init__.py`
- `tests/unit/test_task_model.py`
- `tests/unit/test_task_service.py`
- `tests/integration/__init__.py`
- `tests/integration/test_cli_flow.py`
- `pyproject.toml`
- `README.md`
- `.gitignore`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 + US2 (P1): Can proceed in parallel, form MVP together
  - US3 (P2): Can start after Foundational, uses get_task from service
  - US4-US6 (P3): Can proceed in parallel after Foundational
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Priority | Dependencies | Can Parallelize With |
|-------|----------|--------------|---------------------|
| US1 - Add Task | P1 | Phase 2 only | US2 |
| US2 - View Tasks | P1 | Phase 2 only | US1 |
| US3 - Mark Complete | P2 | Phase 2 only | US4, US5, US6 |
| US4 - Update Task | P3 | Phase 2 only | US3, US5, US6 |
| US5 - Delete Task | P3 | Phase 2 only | US3, US4, US6 |
| US6 - Exit App | P3 | Phase 2 only | US3, US4, US5 |

### Task Count Summary

| Phase | Task Count | Stories Covered | Status |
|-------|------------|-----------------|--------|
| Phase 1: Setup | 4 | - | ✅ |
| Phase 2: Foundational | 6 | - | ✅ |
| Phase 3: US1 Add Task | 6 | P1 | ✅ |
| Phase 4: US2 View Tasks | 6 | P1 | ✅ |
| Phase 5: US3 Mark Complete | 7 | P2 | ✅ |
| Phase 6: US4 Update Task | 4 | P3 | ✅ |
| Phase 7: US5 Delete Task | 4 | P3 | ✅ |
| Phase 8: US6 Exit App | 3 | P3 | ✅ |
| Phase 9: Polish | 7 | - | ✅ |
| **Total** | **47** | **6 stories** | **✅** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
