import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export default function MarkdownMessage({ content, isUser = false }) {
  if (isUser) {
    // User messages are plain text
    return <span>{content}</span>
  }

  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      className="markdown-content"
      components={{
        // Headings
        h1: ({ node, ...props }) => (
          <h1 className="text-xl font-bold mb-3 mt-4 text-ink-100" {...props} />
        ),
        h2: ({ node, ...props }) => (
          <h2 className="text-lg font-semibold mb-2 mt-3 text-ink-100" {...props} />
        ),
        h3: ({ node, ...props }) => (
          <h3 className="text-base font-semibold mb-2 mt-3 text-ink-100" {...props} />
        ),
        
        // Paragraphs
        p: ({ node, ...props }) => (
          <p className="mb-3 text-ink-200 leading-relaxed" {...props} />
        ),
        
        // Lists
        ul: ({ node, ...props }) => (
          <ul className="list-disc list-inside mb-3 space-y-1 text-ink-200" {...props} />
        ),
        ol: ({ node, ...props }) => (
          <ol className="list-decimal list-inside mb-3 space-y-1 text-ink-200" {...props} />
        ),
        li: ({ node, ...props }) => (
          <li className="ml-2 text-ink-200" {...props} />
        ),
        
        // Bold and italic
        strong: ({ node, ...props }) => (
          <strong className="font-semibold text-ink-100" {...props} />
        ),
        em: ({ node, ...props }) => (
          <em className="italic text-ink-200" {...props} />
        ),
        
        // Code blocks
        code: ({ node, inline, ...props }) => {
          if (inline) {
            return (
              <code
                className="bg-ink-800 px-1.5 py-0.5 rounded text-sm font-mono text-accent"
                {...props}
              />
            )
          }
          return (
            <code
              className="block bg-ink-900 p-4 rounded-lg overflow-x-auto my-3 text-sm font-mono text-ink-200"
              {...props}
            />
          )
        },
        pre: ({ node, ...props }) => (
          <pre className="bg-ink-900 p-4 rounded-lg overflow-x-auto my-3" {...props} />
        ),
        
        // Links
        a: ({ node, ...props }) => (
          <a
            className="text-accent hover:text-accent-dark underline"
            target="_blank"
            rel="noopener noreferrer"
            {...props}
          />
        ),
        
        // Tables
        table: ({ node, ...props }) => (
          <div className="overflow-x-auto my-4">
            <table className="min-w-full border-collapse border border-ink-700 rounded-lg" {...props} />
          </div>
        ),
        thead: ({ node, ...props }) => (
          <thead className="bg-ink-800" {...props} />
        ),
        tbody: ({ node, ...props }) => (
          <tbody className="bg-ink-900/50" {...props} />
        ),
        tr: ({ node, ...props }) => (
          <tr className="border-b border-ink-700" {...props} />
        ),
        th: ({ node, ...props }) => (
          <th
            className="px-4 py-2 text-left text-sm font-semibold text-ink-100 border border-ink-700"
            {...props}
          />
        ),
        td: ({ node, ...props }) => (
          <td
            className="px-4 py-2 text-sm text-ink-200 border border-ink-700"
            {...props}
          />
        ),
        
        // Blockquotes
        blockquote: ({ node, ...props }) => (
          <blockquote
            className="border-l-4 border-accent/50 pl-4 my-3 italic text-ink-300"
            {...props}
          />
        ),
        
        // Horizontal rule
        hr: ({ node, ...props }) => (
          <hr className="my-4 border-ink-700" {...props} />
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  )
}

