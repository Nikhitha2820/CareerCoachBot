
const express = require("express");
const multer = require("multer");
const path = require("path");
const router = express.Router();

// configure multer storage
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "uploads/"); // make sure uploads/ folder exists
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + path.extname(file.originalname));
  },
});

const upload = multer({ storage });

router.post("/", upload.single("resume"), (req, res) => {
  console.log("File received: ", req.file);
  res.status(200).json({ message: "File uploaded successfully!" });
});

module.exports = router;