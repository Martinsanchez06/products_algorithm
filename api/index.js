import express from "express";
import {pool} from './db.js'

const app = express()

app.get('/data', async (req, res) => {
    const [result] = await pool.query('select * from CosmeticsProducts')
    res.json(result)
})

app.listen(3004)
console.log("Server running on port 3004");