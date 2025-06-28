const express = require("express");
const session = require("express-session");
const SQLiteStore = require("connect-sqlite3");
const bcrypt = require("bcryptjs");
const cors = require("cors");
const Database = require("better-sqlite3");

const app = express();
const port = 4000;

// session store in sqlite
const SQLiteStoreSession = SQLiteStore(session);

app.use(
  session({
    store: new SQLiteStoreSession({ db: "sessions.sqlite" }),
    secret: "super-secret", // store this securely
    resave: false,
    saveUninitialized: false,
    cookie: {
      maxAge: 1000 * 60 * 60 * 24, // 1 day
    },
  })
);

app.use(cors({
  origin: "http://localhost:3000", 
  credentials: true
}));

app.use(express.json());

// sqlite db
const db = new Database("users.db");

// initialize table if not present
db.prepare(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
  )
`).run();

// register
app.post("/api/register", async (req, res) => {
  const { email, password } = req.body;
  const hashed = await bcrypt.hash(password, 10);

  try {
    db.prepare(`INSERT INTO users (email, password) VALUES (?, ?)`).run(email, hashed);
    res.json({ message: "User registered successfully" });
  } catch (e) {
    if (e.code === "SQLITE_CONSTRAINT_UNIQUE") {
      return res.status(400).json({ error: "Email already exists" });
    }
    console.error(e);
    res.status(500).json({ error: "Registration failed" });
  }
});

// login
app.post("/api/login", async (req, res) => {
  const { email, password } = req.body;

  const user = db.prepare(`SELECT * FROM users WHERE email = ?`).get(email);
  if (!user) return res.status(400).json({ error: "Invalid email or password" });

  const isMatch = await bcrypt.compare(password, user.password);
  if (!isMatch) return res.status(400).json({ error: "Invalid email or password" });

  req.session.userId = user.id;
  res.json({ message: "Login successful" });
});


// logout
app.post("/api/logout", (req, res) => {
  req.session.destroy(() => {
    res.json({ message: "Logged out" });
  });
});

app.listen(port, () => {
  console.log(`Server listening on http://localhost:${port}`);
});
