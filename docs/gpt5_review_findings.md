# GPT-5 Security & Performance Review

## Critical Issues Found

### 🔴 HIGH Priority

1. **Security: Prompt Injection in Card Pool Selection**
   - User question can manipulate JSON output
   - Need strict validation against 78-card allowlist
   - Clamp pool_size to [30,40], weights to [0,3]

2. **Security: Client-side API Keys**
   - Keys exposed in browser
   - Should use backend proxy for production

3. **Performance: Excessive Re-renders**
   - Streaming updates cause too many DOM updates
   - Need throttling (16-50ms batches)

### 🟡 MEDIUM Priority

1. **Streaming: Missing TextDecoder Flush**
   - Can lose final tokens
   - SSE spec not fully followed

2. **Language Detection**
   - Pattern-based is unreliable
   - Needs confidence scoring

3. **Accessibility**
   - Tooltips keyboard/touch inaccessible
   - Missing aria-live for streaming text
   - No prefers-reduced-motion support

### 🟢 LOW Priority

1. **Error Handling**
   - Silent JSON parse failures
   - No timeout/retry logic
   - Missing abort controls

2. **UX Polish**
   - No copy/share buttons
   - Missing language selector UI

## Implemented Fixes

### ✅ Already Fixed
- Reversed card display (image only rotates)
- Basic multilingual support
- Streaming response support
- Intelligent card selection

### 🔧 To Implement
1. Add input validation for card pool JSON
2. Throttle streaming updates
3. Add aria-live regions
4. Implement abort controllers
5. Add error boundaries

## Recommendations

### Immediate Actions
1. Validate all LLM JSON responses
2. Add throttling to streaming
3. Implement basic accessibility fixes

### Future Improvements
1. Move API calls to backend
2. Add proper language detection library
3. Implement retry logic
4. Add telemetry/monitoring