# Image Processing Pipeline

Handle various image inputs:

## OCR Pipeline (Documents)
1. Detect image type (screenshot, document, photo)
2. Extract text using OCR
3. Structure extracted data
4. Store in appropriate location:
   - Screenshots → memory/screenshots/
   - Documents → context/documents/
   - Diagrams → memory/diagrams/

## Visual Analysis
- Describe image contents
- Extract key information
- Identify action items
- Create searchable metadata

## Common Use Cases
- **Whiteboard photo** → Extract notes, create tasks
- **Receipt image** → Log expense, extract data
- **Screenshot** → Parse UI, extract text
- **Diagram** → Document architecture, create mermaid version

Store metadata in memory/images/index.json:
{
  "imageId": "[hash]",
  "type": "[screenshot|document|photo|diagram]",
  "extractedText": "[OCR result]",
  "entities": ["detected entities"],
  "tags": ["auto-generated tags"],
  "actions": ["created tasks or items"],
  "timestamp": "[when processed]"
}
