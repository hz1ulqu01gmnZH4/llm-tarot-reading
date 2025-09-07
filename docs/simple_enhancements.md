# Simple Tarot App Enhancements

## Three Quick Wins (1 Hour Each)

### 1. Dark Mode Toggle
```javascript
// Add to index.html
const darkMode = localStorage.getItem('darkMode') === 'true';
if (darkMode) document.body.classList.add('dark');

document.body.insertAdjacentHTML('afterbegin', 
  '<button onclick="document.body.classList.toggle(\'dark\'); localStorage.setItem(\'darkMode\', document.body.classList.contains(\'dark\'))" style="position:fixed;top:10px;right:10px">🌙</button>'
);
```

```css
/* Add to CSS */
.dark { background: #1a1a1a; color: #fff; }
.dark .card { box-shadow: 0 4px 8px rgba(255,255,255,0.1); }
```

### 2. Save Readings
```javascript
// Save after interpretation
const saveReading = () => {
  const readings = JSON.parse(localStorage.getItem('readings') || '[]');
  readings.push({
    date: new Date().toISOString(),
    question: document.querySelector('#question').value,
    cards: currentCards,
    interpretation: document.querySelector('.interpretation').innerText
  });
  localStorage.setItem('readings', JSON.stringify(readings));
};

// View history
const viewHistory = () => {
  const readings = JSON.parse(localStorage.getItem('readings') || '[]');
  console.table(readings);
};
```

### 3. Better Card Flip
```css
/* Smooth 3D flip */
.card {
  transform-style: preserve-3d;
  transition: transform 0.6s;
}
.card.flipped { transform: rotateY(180deg); }
.card:hover { transform: translateY(-5px); }
```

## Next Level (If Needed)

### Card Zoom
```javascript
// Click to zoom
document.querySelectorAll('.card').forEach(card => {
  card.onclick = () => {
    card.classList.toggle('zoomed');
    document.body.classList.toggle('dimmed');
  };
});
```

```css
.zoomed { 
  transform: scale(1.5); 
  z-index: 100; 
  position: relative;
}
.dimmed { 
  opacity: 0.3; 
}
.dimmed .zoomed { 
  opacity: 1; 
}
```

### Sound Effects
```javascript
// Card flip sound
const playSound = () => {
  const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBTGHz/DUiTYIG2O47OScTgwOUann7blmFgU7k9z1unEiBC13yO/eizEIHWq+8+OWT');
  audio.play();
};
```

### Moon Phase
```javascript
// Simple moon phase calculator
const getMoonPhase = () => {
  const phases = ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'];
  const day = new Date().getDate();
  return phases[Math.floor((day % 30) / 3.75)];
};

document.body.insertAdjacentHTML('afterbegin', 
  `<div style="position:fixed;top:10px;left:10px">${getMoonPhase()}</div>`
);
```

## That's It!

Start with the three quick wins. Add more only if users ask for it.