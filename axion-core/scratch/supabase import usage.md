import { supabase } from '@/logic/supabase';

const { data, error } = await supabase.from('memory_entries').select();
