// [OMEGA AST Cleaned]: Tokenized design standards applied.
import React, { Component, ErrorInfo, ReactNode } from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";

interface Props {
  children?: ReactNode;
  componentName?: string;
  /** If true, renders a compact inline fallback instead of full-page */
  inline?: boolean;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

/**
 * Phoenix Down Protocol — Error Boundary
 * Catches JS errors in the subtree, logs them, and renders a
 * sovereign fallback UI instead of a blank crash.
 */
export class ErrorBoundary extends Component<Props, State> {
  public state: State = { hasError: false, error: null };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    const componentName = this.props.componentName ?? "Unknown Module";
    console.error(`[Phoenix Down] Caught in <${componentName}>:`, error, errorInfo);
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  public render() {
    if (!this.state.hasError) return this.props.children;

    const name = this.props.componentName ?? "cognitive module";
    const message = this.state.error?.message ?? "An unknown error occurred.";

    if (this.props.inline) {
      return (
        <div className="flex items-center gap-3 p-3 bg-red-900/20 border border-red-500/30 rounded-lg text-red-300 text-xs font-mono">
          <AlertTriangle className="w-4 h-4 shrink-0 text-red-400" />
          <span className="truncate">{name}: {message}</span>
          <button
            onClick={this.handleReset}
            className="ml-auto shrink-0 text-red-400 hover:text-red-200 transition-colors cursor-pointer"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>
      );
    }

    return (
      <div className="w-full h-full min-h-[200px] flex flex-col items-center justify-center gap-4 p-8 bg-red-900/10 border border-red-500/30 rounded-xl text-red-200 animate-appear">
        <AlertTriangle className="w-10 h-10 text-red-400 drop-shadow-[0_0_12px_rgba(239,68,68,0.5)]" />
        <div className="text-center space-y-1">
          <h3 className="text-sm font-bold uppercase tracking-widest">Subsystem Anomaly</h3>
          <p className="text-xs text-red-300/70">
            The <span className="font-semibold text-red-300">{name}</span> encountered a critical rendering error.
          </p>
        </div>
        <p className="text-[11px] font-mono bg-black/40 border border-red-500/20 px-3 py-2 rounded max-w-full text-center text-red-300/60 break-all">
          {message}
        </p>
        <button
          onClick={this.handleReset}
          className="flex items-center gap-2 px-4 py-2 min-h-[36px] bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-300 hover:text-red-100 rounded text-xs font-semibold transition-all cursor-pointer"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Attempt Recovery
        </button>
      </div>
    );
  }
}

export default ErrorBoundary;
