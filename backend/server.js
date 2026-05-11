const multer = require("multer");
const pdfParse = require("pdf-parse");
const fs = require("fs");
const path = require("path");

const express = require("express");
const cors = require("cors");

const app = express();

// middleware
app.use(cors());
app.use(express.json());

// test route
app.get("/", (req, res) => {
    res.send("Backend is running successfully 🚀");
});

// start server
app.listen(5000, () => {
    console.log("Server running on http://localhost:5000");
});
const axios = require("axios");

app.post("/analyze", async (req, res) => {
    try {
        const response = await axios.post("http://localhost:8000/analyze", {
            text: "I know Python and SQL"
        });

        res.json(response.data);
    } catch (error) {
        res.status(500).send("Error connecting to ML service");
    }
});
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, "uploads/");
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + "-" + file.originalname);
    }
});

const upload = multer({ storage: storage });
app.post("/upload-resume", upload.single("resume"), async (req, res) => {
    try {
        const filePath = req.file.path;

        // Read PDF
        const dataBuffer = fs.readFileSync(filePath);
        const pdfData = await pdfParse(dataBuffer);

        const extractedText = pdfData.text;

        // Send to ML service
        const response = await axios.post("http://127.0.0.1:8000/analyze", {
            text: extractedText
        });

        res.json({
            extractedText,
            analysis: response.data
        });

    } catch (error) {
        console.error(error);
        res.status(500).send("Error processing resume");
    }
});
