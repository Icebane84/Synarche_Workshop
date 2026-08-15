-- Create the tasks table
create table public.tasks (
  id text primary key, -- Text based ID to match existing 'TASK-XXXXXX' format
  title text not null,
  notes text,
  status text not null, -- 'To Do', 'In Progress', 'Completed'
  source text not null, -- 'Manual', 'Dissonance Scanner', etc.
  priority text not null default 'Medium',
  timestamp timestamptz not null default now(),
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Enable Row Level Security (RLS)
alter table public.tasks enable row level security;

-- Create policy to allow full access (for now, assuming single-tenant/local dev)
-- In production, this should be restricted to authenticated users.
create policy "Allow full access to tasks"
on public.tasks
for all
using (true)
with check (true);

-- Create a function to handle timestamp updates
create or replace function public.handle_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

-- Create trigger for updated_at
create trigger tasks_updated_at
before update on public.tasks
for each row
execute procedure public.handle_updated_at();
