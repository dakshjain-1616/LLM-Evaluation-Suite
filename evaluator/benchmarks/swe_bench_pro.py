"""SWE-Bench Pro — harder agentic coding tasks (full repo context, multi-file fixes)."""
import re
from .base import Benchmark, BenchmarkConfig


class SWEBenchProBenchmark(Benchmark):
    def __init__(self):
        super().__init__(BenchmarkConfig(
            name="swe_bench_pro", description="SWE-Bench Pro agentic coding", category="code",
            timeout=180, max_tokens=4096, temperature=0.2
        ))

    def _load_prompts(self):
        self.prompts = [
            {"id": "swep_001", "prompt": """You are an expert software engineer. Fix the following bug in a Django ORM codebase.

Repository: django/django
Issue: QuerySet.prefetch_related() fails silently when combined with .only() — related objects are fetched but fields specified in only() are ignored for the prefetched queryset.

Relevant code in `django/db/models/query.py`:
```python
def prefetch_related(self, *lookups):
    clone = self._chain()
    if lookups == (None,):
        clone._prefetch_related_lookups = ()
    else:
        for lookup in lookups:
            if isinstance(lookup, Prefetch):
                lookup = lookup.prefetch_to
            lookup = lookup.split(LOOKUP_SEP, 1)[0]
            if lookup in self.query._filtered_relations:
                raise ValueError('prefetch_related() is not supported with FilteredRelation.')
        clone._prefetch_related_lookups = clone._prefetch_related_lookups + lookups
    return clone
```

The bug: when `.only('id', 'name')` is chained before `.prefetch_related('tags')`, the deferred loading mask isn't propagated to the prefetch queryset. Fix this so the deferred fields are respected.

Provide the corrected implementation.""",
             "expected_keywords": ["deferred", "only", "prefetch", "mask", "add_immediate_loading"]},

            {"id": "swep_002", "prompt": """Fix this Python asyncio race condition:

```python
import asyncio
from typing import Dict, Any

class AsyncCache:
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._lock = asyncio.Lock()

    async def get_or_set(self, key: str, factory) -> Any:
        if key in self._cache:
            return self._cache[key]
        async with self._lock:
            value = await factory()
            self._cache[key] = value
            return value
```

Bug: Double-check locking pattern is broken — multiple coroutines pass the first `if` check before the lock is acquired, leading to factory() being called multiple times. Fix with correct double-checked locking.""",
             "expected_keywords": ["async with", "self._lock", "if key in", "double"]},

            {"id": "swep_003", "prompt": """Fix this memory leak in a Python web server connection pool:

```python
class ConnectionPool:
    def __init__(self, max_size=10):
        self._pool = []
        self._max_size = max_size
        self._semaphore = threading.Semaphore(max_size)

    def acquire(self):
        self._semaphore.acquire()
        if self._pool:
            return self._pool.pop()
        return self._create_connection()

    def release(self, conn):
        if conn.is_alive():
            self._pool.append(conn)
        self._semaphore.release()

    def _create_connection(self):
        conn = Connection()
        return conn
```

Bug: When `conn.is_alive()` returns False, the connection is discarded but the pool can grow beyond max_size on next acquire because discarded connections aren't tracked. Fix the pool to maintain correct size.""",
             "expected_keywords": ["semaphore", "max_size", "is_alive", "close", "len"]},

            {"id": "swep_004", "prompt": """You're debugging a Rust ownership error. Fix this code:

```rust
use std::collections::HashMap;

fn process_data(data: &mut HashMap<String, Vec<i32>>) -> Vec<String> {
    let mut result = Vec::new();
    for (key, values) in data.iter() {
        if values.len() > 5 {
            data.remove(key);  // Error: cannot borrow `*data` as mutable
            result.push(key.clone());
        }
    }
    result
}
```

Fix the borrow checker error while preserving the original behavior: remove keys with more than 5 values and return the removed keys.""",
             "expected_keywords": ["collect", "retain", "drain", "keys_to_remove", "iter_mut"]},

            {"id": "swep_005", "prompt": """Fix this SQL N+1 query problem in SQLAlchemy:

```python
from sqlalchemy.orm import Session
from models import User, Post, Comment

def get_user_feed(session: Session, user_ids: list[int]) -> dict:
    result = {}
    users = session.query(User).filter(User.id.in_(user_ids)).all()
    for user in users:
        posts = session.query(Post).filter(Post.user_id == user.id).all()
        result[user.id] = {
            'name': user.name,
            'posts': []
        }
        for post in posts:
            comments = session.query(Comment).filter(Comment.post_id == post.id).all()
            result[user.id]['posts'].append({
                'title': post.title,
                'comment_count': len(comments)
            })
    return result
```

Rewrite to use a single efficient query with proper joins/subqueries.""",
             "expected_keywords": ["joinedload", "subqueryload", "join", "func.count", "options"]},

            {"id": "swep_006", "prompt": """Fix this TypeScript type error and logic bug:

```typescript
interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  loading: boolean;
}

async function fetchWithRetry<T>(
  url: string,
  retries: number = 3
): Promise<ApiResponse<T>> {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url);
      const data = await response.json() as T;
      return { data, error: null, loading: false };
    } catch (e) {
      if (i === retries) {  // Bug: never true
        return { data: null, error: e.message, loading: false };
      }
      await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i)));
    }
  }
}
```

Fix both the off-by-one logic bug and the TypeScript implicit any error on `e`.""",
             "expected_keywords": ["i === retries - 1", "e instanceof Error", "as Error", "never"]},

            {"id": "swep_007", "prompt": """Fix this Python generator memory issue:

```python
def read_large_csv(filepath: str):
    with open(filepath, 'r') as f:
        lines = f.readlines()  # Loads entire file into memory
    for line in lines:
        yield parse_line(line)

def process_all(filepath: str):
    data = list(read_large_csv(filepath))  # Forces full evaluation
    return aggregate(data)
```

Refactor to use true streaming/lazy evaluation so only one line is in memory at a time, while keeping the aggregate working correctly.""",
             "expected_keywords": ["yield", "for line in f", "csv.reader", "readline", "iter"]},

            {"id": "swep_008", "prompt": """Debug this React useEffect infinite loop:

```javascript
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [preferences, setPreferences] = useState({});

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(data => {
        setUser(data);
        setPreferences({ ...preferences, theme: data.theme });
      });
  }, [userId, preferences]);  // Bug: preferences causes infinite loop

  return <div>{user?.name}</div>;
}
```

Fix the infinite loop while keeping the preferences merge behavior correct.""",
             "expected_keywords": ["useCallback", "functional update", "setPreferences(prev", "remove preferences", "userId"]},

            {"id": "swep_009", "prompt": """Fix this Go goroutine leak:

```go
func fetchAll(urls []string) []string {
    results := make([]string, 0)
    ch := make(chan string)

    for _, url := range urls {
        go func(u string) {
            resp, err := http.Get(u)
            if err != nil {
                return  // goroutine exits but channel never receives
            }
            body, _ := io.ReadAll(resp.Body)
            ch <- string(body)
        }(url)
    }

    for i := 0; i < len(urls); i++ {
        results = append(results, <-ch)  // deadlocks if any goroutine returned early
    }
    return results
}
```

Fix the goroutine leak and deadlock.""",
             "expected_keywords": ["errgroup", "WaitGroup", "ch <- \"\"", "close(ch)", "context"]},

            {"id": "swep_010", "prompt": """Fix this Python decorator that breaks function signatures:

```python
import functools
import time

def retry(max_attempts=3, delay=1.0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
        return wrapper
    return decorator

@retry(max_attempts=3)
def fetch_data(url: str, timeout: int = 30) -> dict:
    '''Fetch data from URL.'''
    pass

# Problem: fetch_data.__name__ is 'wrapper', __doc__ is None, signature lost
```

Fix to preserve the original function's metadata and make it introspectable.""",
             "expected_keywords": ["@functools.wraps", "wraps(func)", "__wrapped__", "__doc__", "__name__"]},

            {"id": "swep_011", "prompt": """Fix this database transaction isolation bug:

```python
from sqlalchemy import create_engine, text
from contextlib import contextmanager

engine = create_engine('postgresql://...')

@contextmanager
def transaction():
    with engine.connect() as conn:
        yield conn

def transfer_funds(from_account: int, to_account: int, amount: float):
    with transaction() as conn:
        balance = conn.execute(
            text("SELECT balance FROM accounts WHERE id = :id"),
            {"id": from_account}
        ).scalar()

        if balance < amount:
            raise ValueError("Insufficient funds")

        # Race condition: another transaction can modify balance here
        conn.execute(text("UPDATE accounts SET balance = balance - :amt WHERE id = :id"),
                    {"amt": amount, "id": from_account})
        conn.execute(text("UPDATE accounts SET balance = balance + :amt WHERE id = :id"),
                    {"amt": amount, "id": to_account})
```

Fix using proper transaction isolation with SELECT FOR UPDATE.""",
             "expected_keywords": ["FOR UPDATE", "SERIALIZABLE", "begin()", "commit", "rollback"]},

            {"id": "swep_012", "prompt": """Fix this Python circular import causing ImportError:

```
# models.py
from services import UserService

class User:
    def get_service(self):
        return UserService()

# services.py
from models import User

class UserService:
    def create(self, name: str) -> User:
        return User(name=name)
```

Resolve the circular dependency using proper architectural pattern without changing the public API.""",
             "expected_keywords": ["TYPE_CHECKING", "lazy import", "from __future__", "Annotated", "interface"]},

            {"id": "swep_013", "prompt": """Fix this C extension memory safety issue:

```c
#include <Python.h>

static PyObject* parse_json_string(PyObject* self, PyObject* args) {
    const char* input;
    if (!PyArg_ParseTuple(args, "s", &input)) {
        return NULL;
    }

    char* buffer = malloc(strlen(input));  // Bug: off-by-one, no null terminator space
    strcpy(buffer, input);

    // process buffer...
    PyObject* result = PyUnicode_FromString(buffer);
    // Bug: buffer never freed if exception occurs in processing
    free(buffer);
    return result;
}
```

Fix both memory safety issues.""",
             "expected_keywords": ["strlen(input) + 1", "free(buffer)", "Py_XDECREF", "goto error", "PyMem_Malloc"]},

            {"id": "swep_014", "prompt": """Debug this Kubernetes operator reconcile loop that causes thrashing:

```python
class AppReconciler:
    def reconcile(self, app_name: str, namespace: str):
        app = self.get_app(app_name, namespace)
        desired_replicas = app.spec.replicas

        deployment = self.get_deployment(app_name, namespace)
        current_replicas = deployment.spec.replicas

        if current_replicas != desired_replicas:
            self.scale_deployment(app_name, namespace, desired_replicas)
            self.update_status(app_name, namespace, {"replicas": desired_replicas})
            # Bug: update_status triggers another reconcile which sees stale state
            return True
        return False
```

Fix the reconcile loop to be idempotent and prevent thrashing.""",
             "expected_keywords": ["generation", "resourceVersion", "observedGeneration", "status.conditions", "patch"]},

            {"id": "swep_015", "prompt": """Fix this Python multiprocessing shared state corruption:

```python
from multiprocessing import Pool, Manager
import time

def process_batch(args):
    shared_dict, items = args
    for item in items:
        current = shared_dict.get(item['key'], 0)
        time.sleep(0.001)  # Simulates processing
        shared_dict[item['key']] = current + item['value']  # Race condition

def parallel_aggregate(data, n_workers=4):
    with Manager() as manager:
        shared = manager.dict()
        batches = [data[i::n_workers] for i in range(n_workers)]
        with Pool(n_workers) as pool:
            pool.map(process_batch, [(shared, b) for b in batches])
        return dict(shared)
```

Fix the race condition using proper synchronization.""",
             "expected_keywords": ["Lock", "manager.Lock()", "with lock", "atomic", "Manager().Lock"]},

            {"id": "swep_016", "prompt": """Fix this broken binary search implementation:

```python
def binary_search(arr: list, target: int) -> int:
    left, right = 0, len(arr)  # Bug 1: should be len(arr) - 1

    while left < right:  # Bug 2: should be <=
        mid = (left + right) / 2  # Bug 3: integer division
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid  # Bug 4: should be mid - 1

    return -1
```

Fix all four bugs and add a test case.""",
             "expected_keywords": ["len(arr) - 1", "left <= right", "//", "mid - 1"]},

            {"id": "swep_017", "prompt": """Fix this React state management bug causing stale closures:

```javascript
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(count + 1);  // Stale closure: count is always 0
    }, 1000);
    return () => clearInterval(interval);
  }, []);  // Empty deps intentional but causes bug

  return <div>{count}</div>;
}
```

Fix using functional update pattern to avoid stale closures.""",
             "expected_keywords": ["setCount(prev", "setCount(c =>", "functional update", "count + 1"]},

            {"id": "swep_018", "prompt": """Fix this Python class that violates Liskov Substitution Principle causing runtime errors:

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h
    def area(self): return self.width * self.height

class Square(Rectangle):
    def set_width(self, w):
        self.width = w
        self.height = w  # Violates LSP

    def set_height(self, h):
        self.width = h
        self.height = h

def test_rectangle(rect: Rectangle):
    rect.set_width(4)
    rect.set_height(5)
    assert rect.area() == 20  # Fails for Square
```

Refactor to fix the LSP violation.""",
             "expected_keywords": ["Shape", "abstract", "ABC", "separate", "composition"]},

            {"id": "swep_019", "prompt": """Fix this WebSocket server that drops messages under load:

```python
import asyncio
import websockets

connected_clients = set()
message_queue = asyncio.Queue()

async def handler(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            await message_queue.put(message)
    finally:
        connected_clients.remove(websocket)

async def broadcast():
    while True:
        message = await message_queue.get()
        # Bug: slow clients block broadcast for all others
        for client in connected_clients:
            await client.send(message)  # Blocks if client is slow
```

Fix to prevent slow clients from blocking broadcasts to other clients.""",
             "expected_keywords": ["asyncio.gather", "create_task", "per-client queue", "timeout", "wait_for"]},

            {"id": "swep_020", "prompt": """Fix this critical security vulnerability — SQL injection in a Python web API:

```python
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/users/search')
def search_users():
    name = request.args.get('name', '')
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    # CRITICAL: SQL injection vulnerability
    query = f"SELECT id, name, email FROM users WHERE name LIKE '%{name}%'"
    results = cursor.execute(query).fetchall()
    return {'users': [{'id': r[0], 'name': r[1], 'email': r[2]} for r in results]}
```

Fix the SQL injection and add input validation.""",
             "expected_keywords": ["parameterized", "?", ":name", "cursor.execute(query,", "sanitize"]},
        ]

    def evaluate_response(self, prompt_data: dict, response: str) -> dict:
        keywords = prompt_data.get("expected_keywords", [])
        response_lower = response.lower()
        hits = sum(1 for kw in keywords if kw.lower() in response_lower)
        score = hits / len(keywords) if keywords else 0.5
        has_code = "```" in response or "def " in response or "function " in response or "func " in response
        if has_code:
            score = min(1.0, score + 0.1)
        return {"success": score > 0.4, "score": round(score, 4), "metadata": {"keyword_hits": hits}}

    def get_system_prompt(self):
        return "You are an expert software engineer. Provide precise, working code fixes with explanations."
