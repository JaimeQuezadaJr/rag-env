import { useState, useEffect, useRef } from 'react'
import { 
  FileText, 
  Upload, 
  Send, 
  Trash2, 
  Loader2, 
  MessageSquare,
  Sparkles,
  X,
  CheckCircle2,
  AlertCircle
} from 'lucide-react'
import MarkdownMessage from './MarkdownMessage.jsx'

// Use /api prefix in production (proxied by nginx), direct URL in development
const API_BASE = import.meta.env.VITE_API_BASE || 
  (import.meta.env.PROD ? '/api' : 'http://localhost:8000')

function App() {
  const [pdfs, setPdfs] = useState([])
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isUploading, setIsUploading] = useState(false)
  const [isIngesting, setIsIngesting] = useState(false)
  const [isChatting, setIsChatting] = useState(false)
  const [isReady, setIsReady] = useState(false)
  const [notification, setNotification] = useState(null)
  
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)

  useEffect(() => {
    fetchPdfs()
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 4000)
  }

  const fetchPdfs = async () => {
    try {
      const res = await fetch(`${API_BASE}/pdfs`)
      const data = await res.json()
      setPdfs(data.pdfs)
    } catch (err) {
      console.error('Failed to fetch PDFs:', err)
    }
  }

  const handleUpload = async (e) => {
    const files = Array.from(e.target.files)
    if (files.length === 0) return

    setIsUploading(true)
    
    for (const file of files) {
      const formData = new FormData()
      formData.append('file', file)
      
      try {
        await fetch(`${API_BASE}/upload`, {
          method: 'POST',
          body: formData
        })
      } catch (err) {
        showNotification(`Failed to upload ${file.name}`, 'error')
      }
    }
    
    await fetchPdfs()
    setIsUploading(false)
    showNotification(`Uploaded ${files.length} file(s)`)
    
    // Automatically trigger ingestion after upload
    setIsIngesting(true)
    try {
      const res = await fetch(`${API_BASE}/ingest`, {
        method: 'POST'
      })
      const data = await res.json()
      
      if (data.success) {
        showNotification(`Processed ${data.chunks} chunks from ${data.loaded.length} PDFs`)
        // Show "Ready to chat" status after notification appears
        setTimeout(() => {
          setIsReady(true)
        }, 6000)
      } else {
        showNotification(data.message, 'error')
      }
    } catch (err) {
      showNotification('Auto-processing failed', 'error')
    }
    setIsIngesting(false)
    
    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleDelete = async (filename) => {
    setIsIngesting(true)
    try {
      const res = await fetch(`${API_BASE}/pdfs/${encodeURIComponent(filename)}`, {
        method: 'DELETE'
      })
      const data = await res.json()
      
      await fetchPdfs()
      
      // Check if ingestion was successful
      if (data.ingestion && data.ingestion.success) {
        showNotification(`Deleted ${filename} and rebuilt vectorstore`)
        // Show "Ready to chat" status after notification appears
        setTimeout(() => {
          setIsReady(true)
        }, 6000)
      } else {
        setIsReady(false)
        showNotification(`Deleted ${filename}`, 'error')
      }
    } catch (err) {
      setIsReady(false)
      showNotification('Failed to delete file', 'error')
    }
    setIsIngesting(false)
  }

  const handleIngest = async () => {
    if (pdfs.length === 0) {
      showNotification('Upload some PDFs first', 'error')
      return
    }

    setIsIngesting(true)
    
    try {
      const res = await fetch(`${API_BASE}/ingest`, {
        method: 'POST'
      })
      const data = await res.json()
      
      if (data.success) {
        setIsReady(true)
        showNotification(`Processed ${data.chunks} chunks from ${data.loaded.length} PDFs`)
      } else {
        showNotification(data.message, 'error')
      }
    } catch (err) {
      showNotification('Ingestion failed', 'error')
    }
    
    setIsIngesting(false)
  }

  const handleSend = async () => {
    if (!input.trim() || isChatting) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsChatting(true)

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      })
      const data = await res.json()
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.answer,
        sources: data.sources
      }])
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        sources: []
      }])
    }

    setIsChatting(false)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 px-4 py-3 rounded-lg shadow-lg ${
          notification.type === 'error' 
            ? 'bg-red-500/20 border border-red-500/30 text-red-300' 
            : 'bg-emerald-500/20 border border-emerald-500/30 text-emerald-300'
        }`}>
          {notification.type === 'error' ? <AlertCircle size={18} /> : <CheckCircle2 size={18} />}
          <span className="text-sm">{notification.message}</span>
        </div>
      )}

      {/* Header */}
      <header className="border-b border-ink-800/50 bg-ink-950/80 backdrop-blur-sm sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-accent to-accent-dark flex items-center justify-center">
              <Sparkles size={18} className="text-white" />
            </div>
            <div>
              <h1 className="text-lg font-semibold text-white">DocChat</h1>
              <p className="text-xs text-ink-400">AI Document Assistant</p>
            </div>
          </div>
          
          {isReady && (
            <div className="flex items-center gap-2 text-sm text-emerald-400">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              Ready to chat
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex max-w-6xl mx-auto w-full">
        {/* Sidebar - Document Management */}
        <aside className="w-80 border-r border-ink-800/50 p-6 flex flex-col">
          <div className="mb-6">
            <h2 className="text-sm font-medium text-ink-300 uppercase tracking-wider mb-4">
              Documents
            </h2>
            
            {/* Upload Button */}
            <label className={`
              flex items-center justify-center gap-2 w-full py-3 px-4 rounded-lg
              border-2 border-dashed border-ink-700 hover:border-accent/50
              bg-ink-900/30 hover:bg-ink-900/50
              text-ink-400 hover:text-accent
              cursor-pointer transition-all duration-200
              ${isUploading ? 'opacity-50 pointer-events-none' : ''}
            `}>
              {isUploading ? (
                <Loader2 size={18} className="animate-spin" />
              ) : (
                <Upload size={18} />
              )}
              <span className="text-sm font-medium">
                {isUploading ? 'Uploading...' : 'Upload PDFs'}
              </span>
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                multiple
                onChange={handleUpload}
                className="hidden"
                disabled={isUploading}
              />
            </label>
          </div>

          {/* PDF List */}
          <div className="flex-1 overflow-y-auto space-y-2">
            {pdfs.length === 0 ? (
              <div className="text-center py-8 text-ink-500">
                <FileText size={32} className="mx-auto mb-2 opacity-50" />
                <p className="text-sm">No documents yet</p>
              </div>
            ) : (
              pdfs.map((pdf) => (
                <div
                  key={pdf}
                  className="group flex items-center gap-3 p-3 rounded-lg bg-ink-900/30 hover:bg-ink-900/50 transition-colors"
                >
                  <FileText size={16} className="text-ink-500 flex-shrink-0" />
                  <span className="text-sm text-ink-300 truncate flex-1" title={pdf}>
                    {pdf}
                  </span>
                  <button
                    onClick={() => handleDelete(pdf)}
                    className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-400 transition-all"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              ))
            )}
          </div>

          {/* Process Button */}
          <button
            onClick={handleIngest}
            disabled={isIngesting || pdfs.length === 0}
            className={`
              mt-6 w-full py-3 px-4 rounded-lg font-medium text-sm
              flex items-center justify-center gap-2
              transition-all duration-200
              ${pdfs.length === 0 
                ? 'bg-ink-800 text-ink-500 cursor-not-allowed'
                : isIngesting
                  ? 'bg-accent/20 text-accent cursor-wait'
                  : 'bg-accent hover:bg-accent-dark text-white shadow-lg shadow-accent/20'
              }
            `}
          >
            {isIngesting ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Sparkles size={18} />
                Process Documents
              </>
            )}
          </button>
        </aside>

        {/* Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-ink-500">
                <MessageSquare size={48} className="mb-4 opacity-30" />
                <h3 className="text-lg font-medium text-ink-400 mb-2">Start a conversation</h3>
                <p className="text-sm text-center max-w-sm">
                  Upload your PDFs, process them, then ask questions about the content.
                </p>
              </div>
            ) : (
              messages.map((message, idx) => (
                <div
                  key={idx}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
                >
                  <div
                    className={`max-w-[80%] ${
                      message.role === 'user'
                        ? 'bg-accent text-white rounded-2xl rounded-br-md px-4 py-3'
                        : 'bg-ink-900/50 border border-ink-800/50 rounded-2xl rounded-bl-md px-5 py-4'
                    }`}
                  >
                    <MarkdownMessage 
                      content={message.content} 
                      isUser={message.role === 'user'} 
                    />
                    
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-ink-700/50">
                        <p className="text-xs text-ink-500 mb-1">Sources:</p>
                        <div className="flex flex-wrap gap-1">
                          {message.sources.map((s, i) => (
                            <span
                              key={i}
                              className="text-xs bg-ink-800/50 text-ink-400 px-2 py-0.5 rounded"
                            >
                              {s.pdf} (p.{s.page})
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            
            {isChatting && (
              <div className="flex justify-start animate-fade-in">
                <div className="bg-ink-900/50 border border-ink-800/50 rounded-2xl rounded-bl-md px-5 py-4">
                  <div className="loading-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-ink-800/50 p-4">
            <div className="flex gap-3 items-end">
              <div className="flex-1 relative">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder={isReady ? "Ask about your documents..." : "Process documents first to start chatting"}
                  disabled={!isReady || isChatting}
                  rows={1}
                  className={`
                    w-full resize-none rounded-xl border border-ink-800
                    bg-ink-900/50 px-4 py-3 pr-12
                    text-ink-100 placeholder:text-ink-600
                    focus:outline-none focus:border-accent/50 focus:ring-1 focus:ring-accent/20
                    disabled:opacity-50 disabled:cursor-not-allowed
                    transition-all duration-200
                  `}
                  style={{ minHeight: '48px', maxHeight: '120px' }}
                />
              </div>
              
              <button
                onClick={handleSend}
                disabled={!input.trim() || !isReady || isChatting}
                className={`
                  p-3 rounded-xl transition-all duration-200
                  ${!input.trim() || !isReady || isChatting
                    ? 'bg-ink-800 text-ink-600 cursor-not-allowed'
                    : 'bg-accent hover:bg-accent-dark text-white shadow-lg shadow-accent/20'
                  }
                `}
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App

